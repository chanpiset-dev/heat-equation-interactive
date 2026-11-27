// Keep plot dimensions in CSS and allocate their backing stores near the reader.
const visiblePlots = new Set();
const allocatedPlots = new Set();
const plotSizes = new WeakMap();
const plotCallbacks = new WeakMap();
const pendingPlots = new Set();
let plotFrame = 0;

function schedulePlot(draw) {
    pendingPlots.add(draw);
    if (plotFrame || document.hidden) return;
    plotFrame = requestAnimationFrame(() => {
        plotFrame = 0;
        if (document.hidden) return;
        const batch = [...pendingPlots];
        pendingPlots.clear();
        for (const callback of batch) callback();
    });
}

const plotResize = new ResizeObserver(entries => {
    for (const {target, contentRect} of entries) {
        const size = `${contentRect.width}:${contentRect.height}:${plotDpr()}`;
        if (plotSizes.get(target) === size) continue;
        plotSizes.set(target, size);
        if (visiblePlots.has(target)) schedulePlot(plotCallbacks.get(target));
    }
});

const plotVisibility = new IntersectionObserver(entries => {
    for (const {target, isIntersecting, intersectionRect} of entries) {
        if (isIntersecting && intersectionRect.width && intersectionRect.height) {
            visiblePlots.add(target);
            if (target instanceof HTMLCanvasElement) plotResize.observe(target);
            schedulePlot(plotCallbacks.get(target));
        } else {
            visiblePlots.delete(target);
            if (!(target instanceof HTMLCanvasElement)) continue;
            plotResize.unobserve(target);
            plotSizes.delete(target);
            if (allocatedPlots.delete(target)) {
                target.width = target.height = 1;
                delete target._bounds;
            }
        }
    }
}, {rootMargin: '220px 0px'});

function watchPlots(draw, ...ids) {
    for (const id of ids) {
        const target = document.getElementById(id);
        plotCallbacks.set(target, draw);
        plotVisibility.observe(target);
    }
}

function plotDpr() {
    return Math.min(devicePixelRatio || 1, innerWidth <= 1000 ? 1.5 : 2);
}

document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        for (const target of visiblePlots) schedulePlot(plotCallbacks.get(target));
    }
});
