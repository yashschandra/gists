function processGeneric(n, point) {
    let sum = 0;
    for(let i=0; i<n; i++) {
        sum += point.a;
    }
    return sum;
}

function processPoint2(n, point) {
    let sum = 0;
    for(let i=0; i<n; i++) {
        sum += point.a;
    }
    return sum;
}

function processPoint(n, point) {
    let sum = 0;
    for(let i=0; i<n; i++) {
        sum += point.a;
    }
    return sum;
}

function runMain() {
    let warmup = 500;
    let N = 120000000;
    let p1 = {};
    let p2 = {};
    let p3 = {};
    p1.a = 1;
    p2.b = 2;
    p2.a = 1;
    p3.a = 1;
    let sum;
    let start, t1, t2, t3;
    sum = processPoint(warmup, p3);
    start = new Date();
    sum = processPoint(N, p1);
    t1 = new Date() - start;
    sum = processPoint2(warmup, p2);
    start = new Date();
    sum = processPoint2(N, p1);
    t2 = new Date() - start;
    sum = processGeneric(warmup, 1);
    start = new Date();
    sum = processGeneric(N, p1);
    t3 = new Date() - start;
    console.log(t1, t2, t3);
}

(function() {
    runMain();
})();