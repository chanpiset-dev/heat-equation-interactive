(() => {
    const article = document.querySelector('article');
    const contents = document.getElementById('toc');
    const pending = new Set();
    const observed = new Set();
    let running = false;
    const observer = new IntersectionObserver(entries => {
        for (const {target, isIntersecting, intersectionRect} of entries) {
            if (isIntersecting && intersectionRect.height > 0) pending.add(target);
            else pending.delete(target);
        }
        schedule();
    }, {rootMargin: '350px 0px'});

    function watch(root) {
        observed.add(root);
        observer.observe(root);
    }

    function unwatch(root) {
        observer.unobserve(root);
        observed.delete(root);
        pending.delete(root);
    }

    function schedule() {
        if (running || !pending.size || document.hidden) return;
        running = true;
        requestAnimationFrame(renderBatch);
    }

    async function renderBatch() {
        try {
            if (document.hidden) return;
            const heading = document.getElementById(location.hash.slice(1));
            const batch = [...pending].filter(node => node.isConnected).map(node => {
                const {top, bottom} = node.getBoundingClientRect();
                const distance = heading && (node.contains(heading) || heading.contains(node))
                    ? -1 : Math.max(0, top - innerHeight, -bottom);
                return {node, distance};
            }).sort((a, b) => a.distance - b.distance).slice(0, 8).map(item => item.node);
            const roots = batch.filter(node => !batch.some(other => other !== node && node.contains(other)));
            if (!batch.length) return;
            for (const node of roots) {
                unwatch(node);
            }
            await MathJax.typesetPromise(roots);
            document.dispatchEvent(new CustomEvent('articlemathrendered', {detail: roots}));
        } catch (error) {
            console.error('Unable to typeset article math', error);
        } finally {
            running = false;
            schedule();
        }
    }

    // Find complete TeX spans with the same delimiter parser MathJax uses. A root
    // can contain another root, so only queue each container once.
    MathJax.startup.promise.then(() => {
        const doc = MathJax.startup.document;
        doc.findMath({elements: [article, contents]});
        const roots = new Set();
        for (const item of doc.math) {
            let root = item.start.node.parentElement;
            while (!root.contains(item.end.node)) root = root.parentElement;
            roots.add(root.closest('.eq') || root);
        }
        doc.clear().reset();
        for (const root of roots) watch(root);
        const target = document.getElementById(location.hash.slice(1));
        if (target) target.scrollIntoView({behavior: 'instant'});
    });
    window.addEventListener('beforeprint', () => {
        if (!MathJax.startup.document) return;
        MathJax.typeset([article]);
        for (const root of observed) if (article.contains(root)) unwatch(root);
    });
    document.addEventListener('tocmathchanged', ({detail: results}) => {
        for (const root of observed) if (!root.isConnected) unwatch(root);
        for (const link of results.querySelectorAll('a')) {
            if (link.textContent.includes('\\(')) watch(link);
        }
    });
    document.addEventListener('visibilitychange', schedule);
})();
