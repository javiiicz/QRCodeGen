export function padZeroesLeft(string, length) {
    if (length <= string.length) {
        return string;
    }

    const padding = '0'.repeat(length - string.length);
    return padding + string;
}

export function padZeroesRight(string, length) {
    if (length <= string.length) {
        return string;
    }

    const padding = '0'.repeat(length - string.length);
    return string + padding;
}

export function splice(string, k) {
    const groups = [];
    for (let i = 0; i < string.length; i += k) {
        groups.push(string.slice(i, i + k));
    }
    return groups;
}

export function loop(codewords) {
    const res = [];
    const maxI = codewords.g2.length ? Math.max(codewords.g1[0].length, codewords.g2[0].length) : codewords.g1[0].length;

    for (let i = 0; i < maxI; i++) {
        for (const group in codewords) {
            for (const block of codewords[group]) {
                if (i >= block.length) {
                    continue;
                }
                res.push(block[i]);
            }
        }
    }

    return res;
}

export function getPairs(nums) {
    const pairNum = nums.length ** 2;
    const res = Array.from({ length: pairNum }, () => []);

    for (let i = 0; i < nums.length; i++) {
        for (let j = 0; j < nums.length; j++) {
            res[i * nums.length + j].push(nums[i]);
        }
    }
    
    for (let i = 0; i < res.length; i++) {
        res[i].push(nums[i % nums.length]);
    }

    return res;
}

export function score(matrix) {
    let total = 0;
    total += cond1(matrix);
    total += cond2(matrix);
    total += cond3(matrix);
    total += cond4(matrix);
    return total;
}

export function cond1(matrix) {
    let total = 0;

    let currRunX = 1;
    let prevX = null;

    let currRunY = 1;
    let prevY = null;

    for (let i = 0; i < matrix.length; i++) {
        for (let j = 0; j < matrix.length; j++) {
            const bitX = matrix[i][j];
            if (bitX === prevX) {
                currRunX++;
            } else {
                currRunX = 1;
            }
            prevX = bitX;

            if (currRunX === 5) {
                total += 3;
            } else if (currRunX >= 5) {
                total += 1;
            }

            const bitY = matrix[j][i];
            if (bitY === prevY) {
                currRunY++;
            } else {
                currRunY = 1;
            }
            prevY = bitY;

            if (currRunY === 5) {
                total += 3;
            } else if (currRunY >= 5) {
                total += 1;
            }
        }
    }

    return total;
}

export function cond2(matrix) {
    let blocks = 0;

    for (let i = 0; i < matrix.length - 1; i++) {
        for (let j = 0; j < matrix.length - 1; j++) {
            let square = 0;
            square += matrix[i][j];
            square += matrix[i + 1][j];
            square += matrix[i][j + 1];
            square += matrix[i + 1][j + 1];

            if (square === 0 || square === 4) {
                blocks++;
            }
        }
    }

    return blocks * 3;
}

export function cond3(matrix) {
    let total = 0;
    const patterns = ['10111010000', '00001011101'];
    for (let i = 0; i < matrix.length; i++) {
        for (let j = 0; j < matrix.length - 10; j++) {
            let stringX = '';
            let stringY = '';
            for (let k = 0; k < 11; k++) {
                stringX += matrix[i][j + k];
                stringY += matrix[j + k][i];
            }
            if (stringX === patterns[0] || stringX === patterns[1]) {
                total += 40;
            }
            if (stringY === patterns[0] || stringY === patterns[1]) {
                total += 40;
            }
        }
    }
    return total;
}

export function cond4(matrix) {
    let total = 0;
    let dark = 0;

    for (const row of matrix) {
        for (const col of row) {
            total++;
            if (col === 1) {
                dark++;
            }
        }
    }

    let percent = (dark / total) * 100;
    percent = Math.floor(percent);

    let prev = percent - (percent % 5);
    let follow = percent + (5 - (percent % 5));

    prev = Math.abs(prev - 50) / 5;
    follow = Math.abs(follow - 50) / 5;

    return Math.min(prev, follow) * 10;
}

export function formatPrintQr(matrix) {
    for (const row of matrix) {
        for (const col of row) {
            if (col === null) {
                process.stdout.write('_');
            } else if (col === 1) {
                process.stdout.write('  ');
            } else if (col === 2) {
                process.stdout.write('r');
            } else {
                process.stdout.write('██');
            }
        }
        console.log('');
    }
}

