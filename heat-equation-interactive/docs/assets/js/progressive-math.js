(() => {
    const article = document.querySelector('article');
    const contents = document.getElementById('toc');
    const pending = new Set();
    const observed = new Set();
    const nestedRoots = new WeakMap();
    const searchRoots = new Set();
    const printOpened = new Set();
    let frame = 0;

    const observer = new IntersectionObserver(entries => {
        for (const {target, isIntersecting, intersectionRect} of entries) {
            if (!observed.has(target)) continue;
            if (isIntersecting && intersectionRect.width > 0 && intersectionRect.height > 0) {
                pending.add(target);
            } else {
                pending.delete(target);
            }
        }
        schedule();
        // Edge contact is already intersecting at threshold 0. A positive
        // threshold also notifies us when the intersection acquires area.
    }, {rootMargin: '350px 0px', threshold: [0, Number.EPSILON]});

    function watch(root) {
        observed.add(root);
        observer.observe(root);
    }

    function unwatch(root) {
        observer.unobserve(root);
        observed.delete(root);
        pending.delete(root);
    }

    function insideClosedDisclosure(root) {
        if (root.matches('details:not([open])')) return true;
        for (let child = root; child.parentElement; child = child.parentElement) {
            if (child.parentElement.matches('details:not([open])') && !child.matches('summary')) {
                return true;
            }
        }
        return false;
    }

    function schedule() {
        if (!frame && pending.size && !document.hidden) {
            frame = requestAnimationFrame(renderBatch);
        }
    }

    function renderBatch() {
        frame = 0;
        if (document.hidden) return;

        const heading = document.getElementById(location.hash.slice(1));
        const candidates = [];
        for (const root of pending) {
            if (!root.isConnected) {
                unwatch(root);
                continue;
            }
            if (insideClosedDisclosure(root)) {
                pending.delete(root);
                continue;
            }
            const {top, bottom} = root.getBoundingClientRect();
            const distance = heading && (root.contains(heading) || heading.contains(root))
                ? -1 : Math.max(0, top - innerHeight, -bottom);
            candidates.push({root, distance});
        }
        const batch = candidates.sort((a, b) => a.distance - b.distance)
            .slice(0, 8).map(candidate => candidate.root);
        if (!batch.length) return;

        // MathJax scans descendants of each supplied element. Give each
        // registered root ownership of its own math, including when another
        // root is in a collapsed disclosure inside it.
        const roots = batch.filter(root => !batch.some(other => other !== root && other.contains(root)));
        const masked = new Set();
        for (const root of roots) {
            for (const descendant of nestedRoots.get(root) || []) {
                if (!observed.has(descendant) || descendant.classList.contains('mathjax_ignore')) continue;
                descendant.classList.add('mathjax_ignore');
                masked.add(descendant);
            }
        }

        for (const root of roots) pending.delete(root);
        try {
            // The local full TeX/SVG bundle needs no network retries here.
            // A synchronous batch also serializes search and print handlers.
            MathJax.typeset(roots);
            for (const root of roots) unwatch(root);
            document.dispatchEvent(new CustomEvent('articlemathrendered', {detail: roots}));
        } catch (error) {
            console.error('Unable to typeset article math', error);
        } finally {
            for (const root of masked) root.classList.remove('mathjax_ignore');
            schedule();
        }
    }

    MathJax.startup.promise.then(() => {
        // Use MathJax's parser to locate complete spans without typesetting.
        const doc = MathJax.startup.document;
        doc.findMath({elements: [article, contents]});
        const roots = new Set();
        for (const item of doc.math) {
            let root = item.start.node.parentElement;
            while (!root.contains(item.end.node)) root = root.parentElement;
            roots.add(root.closest('.eq') || root);
        }
        doc.clear().reset();

        for (const root of roots) {
            for (let ancestor = root.parentElement; ancestor; ancestor = ancestor.parentElement) {
                if (!roots.has(ancestor)) continue;
                if (!nestedRoots.has(ancestor)) nestedRoots.set(ancestor, []);
                nestedRoots.get(ancestor).push(root);
            }
            watch(root);
        }
        const target = document.getElementById(location.hash.slice(1));
        if (target) target.scrollIntoView({behavior: 'instant'});
    });

    window.addEventListener('beforeprint', () => {
        if (!MathJax.startup.document) return;
        const proofs = article.querySelectorAll('details.proof, details[data-disclosure="proof"]');
        for (const proof of proofs) {
            for (let part = proof; part; part = part.parentElement?.closest('details')) {
                if (part.open) continue;
                printOpened.add(part);
                part.open = true;
            }
        }
        MathJax.typeset([article]);
        for (const root of observed) if (article.contains(root)) unwatch(root);
    });
    window.addEventListener('afterprint', () => {
        for (const proof of printOpened) proof.open = false;
        printOpened.clear();
    });

    document.addEventListener('tocmathchanged', ({detail: results}) => {
        for (const root of searchRoots) unwatch(root);
        searchRoots.clear();
        for (const link of results.querySelectorAll('a')) {
            if (!link.textContent.includes('\\(')) continue;
            searchRoots.add(link);
            watch(link);
        }
    });
    document.addEventListener('toggle', ({target}) => {
        if (target.matches('details[open]') && observed.has(target)) {
            observer.unobserve(target);
            observer.observe(target);
        }
    }, true);
    document.addEventListener('visibilitychange', schedule);
})();
