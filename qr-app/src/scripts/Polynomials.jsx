import { Tables } from './Tables.jsx';

class Polynomial {
    // i in represents a exponent in x^[len - i - 1]
    constructor(c) {
        this.coef = c;
    }

    gf256MultWith(poly2) {
        // Input -> Polynomial obj in alpha notation
        // Output -> Polynomial obj in alpha notation
        let p1 = this.coef;
        let p2 = poly2.coef;
        [p1, p2] = makeSameLength(p1, p2);
        let p3 = new Array(2 * (p1.length - 1) + 1).fill(null);
        
        // Find multiplication factor and multiply every coefficient
        p1.forEach((c1, i) => {
            if (c1 === null) return;
            p2.forEach((c2, j) => {
                if (c2 === null) return;

                let e1 = p1.length - i - 1;
                let e2 = p2.length - j - 1;
                let e3 = e1 + e2;

                if (p3[p3.length - e3 - 1] === null) { 
                    p3[p3.length - e3 - 1] = (c1 + c2) % 255;
                } else {
                    let int1 = Tables.antilog[p3[p3.length - e3 - 1]];
                    let c3 = (c1 + c2) % 255;
                    let int2 = Tables.antilog[c3];
                    let int3 = int1 ^ int2;
                    p3[p3.length - e3 - 1] = Tables.log[int3];
                }
            });
        });

        let res = [];
        p3.forEach(n => {
            if (n !== null) res.push(n);
        });

        return new Polynomial(res);
    }

    gf256DivideBy(poly) {
        // Input -> 1 Polynomial obj in alpha notation
        // Output -> coefficients of remainder of division in int notation
        let dividend = this.coef;
        let divisor = poly.coef;
        let k = dividend.length - divisor.length + 1;

        for (let i = 0; i < k; i++) {
            dividend = divideOnce(dividend, [...divisor]);
        }

        return toInt(dividend);
    }
}

function makeSameLength(p1, p2) {
    if (p1.length === p2.length) return [p1, p2];
    let diff = p1.length - p2.length;
    if (diff > 0) {
        p2 = new Array(diff).fill(null).concat(p2);
    } else {
        diff = -diff;
        p1 = new Array(diff).fill(null).concat(p1);
    }
    return [p1, p2];
}

function divideOnce(dividend, divisor) {
    // input -> 2 coefficient lists | alpha notation
    // output -> coef of remainder from one division in alpha notation
    if (divisor.length > dividend.length) return dividend;

    let factor = dividend[0];
    if (factor === null) return dividend.slice(1);

    // Multiply factor and convert to int
    divisor.forEach((c, i) => {
        if (c === null) {
            divisor[i] = 0;
        } else {
            let e = (c + factor) % 255;
            divisor[i] = Tables.antilog[e];
        }
    });

    dividend = toInt(dividend);

    // Expand divisor coeff
    divisor = divisor.concat(new Array(dividend.length - divisor.length).fill(0));

    // XOR result with message polynomial
    dividend = dividend.map((d2, i) => divisor[i] ^ d2);

    // Discard first (will always be 0)
    dividend = dividend.slice(1);

    return toExp(dividend);
}

function toInt(coef) {
    return coef.map(c => (c === null ? 0 : Tables.antilog[c]));
}

function toExp(coef) {
    return coef.map(c => Tables.log[c]);
}

export {Polynomial, toExp}
