import {Tables} from './Tables.js';
import {Polynomial, toExp} from './Polynomials.js';
import {Patterns} from './Patterns.js';
import * as helper from './Helpers.js';

export class Message {
    constructor(plaintext, level = "L") {
        this.plaintext = plaintext;
        this.mode = "";
        this.level = level;
        this.version = 0;
        this.bits = "";
        this.blocks = null;
        this.ecCodewords = null;
        this.final = [];
        this.size = 0;
        this.matrix = [];
        this.dataMatrix = [];
        this.createQRCode()
    }

    createQRCode() {
        this.analyze()
        this.encode()
        this.generateEcCodewords()
        this.structureMessage()
        this.modulePlacement()
        this.maskData()
        this.finalizeCode()
    }

    //
    // Step 1: Data Analysis
    //
    analyze() {
        let modes = {"numeric": 1, "alphanumeric": 1, "byte": 1, "kanji": 1};

        for (let char of this.plaintext) {
            if (!Tables.numeric.has(char)) {
                modes["numeric"] = 0;
            }
            if (!(char in Tables.alphanumeric)) {
                modes["alphanumeric"] = 0;
            }
            if (!Tables.byte.has(char)) {
                modes["byte"] = 0;
            }
            // if (!Tables.kanji.includes(char)) {    Not going to be implemented for now...
            //     modes["kanji"] = 0;
            // }
        }

        for (let mode in modes) {
            if (modes[mode] === 1) {
                this.mode = mode;
                return;
            }
        }
    }

    //
    // Step 2: Data Encoding
    // 
    encode() {
        this.determineVersion();
        this.addIndicators();
        switch (this.mode) {
            case "numeric":
                this.numericEncode();
                break;
            case "alphanumeric":
                this.alphanumericEncode();
                break;
            case "byte":
                this.byteEncode();
                break;
            case "kanji":
                this.kanjiEncode();
                break;
            default:
                throw new Error("Mode does not exist or has not been determined.");
        }
        this.alignBytes();
    }

    determineVersion() {
        const lookup = Tables.versions;
        const ecLevel = {"L": 0, "M": 1, "Q": 2, "H": 3}[this.level];
        const mode = {"numeric": 0, "alphanumeric": 1, "byte": 2, "kanji": 3}[this.mode];

        if (ecLevel === undefined || mode === undefined) {
            throw new Error("Mode or Error Correction Level not determined.");
        }

        for (let i = 0; i < 40; i++) {
            if (lookup[i][ecLevel][mode] >= this.plaintext.length) {
                this.version = i + 1;
                return;
            }
        }

        throw new Error("String is too big, no version can fit it.");
    }

    addIndicators() {
        // Mode Indicator
        const indicator = {"numeric": "0001", "alphanumeric": "0010", "byte": "0100", "kanji": "1000"};
        this.bits += indicator[this.mode];

        // Character Count Indicator
        const count = this.plaintext.length.toString(2);
        let paddingLookup;
        if (this.version <= 9) {
            paddingLookup = 0;
        } else if (this.version <= 26) {
            paddingLookup = 1;
        } else {
            paddingLookup = 2;
        }
        const mode = {"numeric": 0, "alphanumeric": 1, "byte": 2, "kanji": 3}[this.mode];
        const countIndicatorLen = Tables.padding[paddingLookup][mode];
        this.bits += helper.padZeroesLeft(count, countIndicatorLen);
    }

    numericEncode() {
        let data = "";
        // Separate in groups of 3
        const groups = helper.splice(this.plaintext, 3);

        // Convert to binary
        for (const trio of groups) {
            const num = parseInt(trio, 10);
            let binary = num.toString(2);
            let length;
            if (num > 99) {
                length = 10;
            } else if (num > 9) {
                length = 7;
            } else {
                length = 4;
            }
            binary = helper.padZeroesLeft(binary, length);
            data += binary;
        }

        this.bits += data;
    }

    alphanumericEncode() {
        let data = "";
        // Separate in groups of 2
        const groups = helper.splice(this.plaintext, 2);

        // Convert to binary
        for (const pair of groups) {
            let binary;
            if (pair.length === 1) {
                const num = Tables.alphanumeric[pair];
                binary = num.toString(2);
                binary = helper.padZeroesLeft(binary, 6);
            } else {
                const first = Tables.alphanumeric[pair[0]];
                const second = Tables.alphanumeric[pair[1]];
                const num = (45 * first) + second;
                binary = num.toString(2);
                binary = helper.padZeroesLeft(binary, 11);
            }
            data += binary;
        }

        this.bits += data;
    }

    byteEncode() {
        let data = "";
        for (const char of this.plaintext) {
            let binary = char.charCodeAt(0).toString(2);
            binary = helper.padZeroesLeft(binary, 8);
            data += binary;
        }

        this.bits += data;
    }

    kanjiEncode() {
        throw new Error("Kanji mode not implemented.");
    }

    alignBytes() {
        // Add Terminator
        const bitsNecessary = this.determineBits();
        let diff = bitsNecessary - this.bits.length;
        if (diff > 4) {
            this.bits = helper.padZeroesRight(this.bits, this.bits.length + 4);
        } else {
            this.bits = helper.padZeroesRight(this.bits, this.bits.length + diff);
        }

        // Make multiple of 8
        if (this.bits.length % 8 !== 0) {
            this.bits = helper.padZeroesRight(this.bits, (8 - (this.bits.length % 8)) + this.bits.length);
        }
        
        
        // Add pad bytes
        const padBytes = "1110110000010001";
        const padBytesNeeded = (bitsNecessary - this.bits.length) / 8;
        if (padBytesNeeded % 2 === 0) {
            this.bits += padBytes.repeat(padBytesNeeded / 2);
        } else {
            this.bits += padBytes.repeat((padBytesNeeded - 1) / 2);
            this.bits += padBytes.slice(0, 8);
        }
    }

    determineBits() {
        const ecLevel = {"L": 0, "M": 1, "Q": 2, "H": 3}[this.level];
        return 8 * Tables.codewords[this.version - 1][ecLevel][0];
    }

    //
    // Step 3: Error Correction
    generateEcCodewords() {
        this.blocks = this.breakIntoBlocks();
        this.ecCodewords = this.getDivisionRemainder(this.blocks);
    }

    breakIntoBlocks() {
        const segments = {g1: [], g2: []};
        const ecLevel = {L: 0, M: 1, Q: 2, H: 3}[this.level];

        const blocksG1 = Tables.codewords[this.version - 1][ecLevel][2];
        const codewordsPerBlockG1 = Tables.codewords[this.version - 1][ecLevel][3];
        const codewordsG1 = codewordsPerBlockG1 * blocksG1;

        const blocksG2 = Tables.codewords[this.version - 1][ecLevel][4];
        const codewordsPerBlockG2 = Tables.codewords[this.version - 1][ecLevel][5];
        
        segments.g1 = helper.splice(this.bits.slice(0, codewordsG1 * 8), codewordsPerBlockG1 * 8);
        if (blocksG2 !== 0) {
            segments.g2 = helper.splice(this.bits.slice(codewordsG1 * 8), codewordsPerBlockG2 * 8);
        }

        for (const group in segments) {
            for (let i = 0; i < segments[group].length; i++) {
                let block = segments[group][i];
                let ints = helper.splice(block, 8);

                for (let j = 0; j < ints.length; j++) {
                    // Convert to integer value
                    ints[j] = parseInt(ints[j], 2);
                }

                segments[group][i] = ints;
            }
        }

        return segments;
    }

    getDivisionRemainder(blocks) {
        const ecLevel = {L: 0, M: 1, Q: 2, H: 3}[this.level];
        const ecPerBlock = Tables.codewords[this.version - 1][ecLevel][1];
        const ecCodewords = {g1: [], g2: []};

        for (const group in blocks) {
            for (const block of blocks[group]) {
                // Alpha notation
                let messageP = toExp([...block]);
                const genP = Tables.gen_p[ecPerBlock];

                // Expand message polynomial
                messageP = messageP.concat(new Array(ecPerBlock).fill(null));

                messageP = new Polynomial(messageP);
                const genPolynomial = new Polynomial(genP);

                // Recall Message Polynomial is degree codewordsPerBlock + ecCodewords
                // Generator polynomial is degree ecCodewords
                ecCodewords[group].push(messageP.gf256DivideBy(genPolynomial));
            }
        }

        return ecCodewords;
    }

    //
    // Step 4: Structure Final Message
    //
    structureMessage() {
        this.final = this.final.concat(helper.loop(this.blocks));
        this.final = this.final.concat(helper.loop(this.ecCodewords));

        // Binary Conversion
        this.bits = "";
        for (const n of this.final) {
            let binary = n.toString(2);
            binary = helper.padZeroesLeft(binary, 8);
            this.bits += binary;
        }

        // Add Remainder bits
        if (this.version >= 2 && this.version < 7) {
            this.bits = helper.padZeroesRight(this.bits, this.bits.length + 7);
        } else if ((this.version >= 14 && this.version < 21) || (this.version >= 28 && this.version < 35)) {
            this.bits = helper.padZeroesRight(this.bits, this.bits.length + 3);
        } else if (this.version >= 21 && this.version < 28) {
            this.bits = helper.padZeroesRight(this.bits, this.bits.length + 4);
        }
    }

    //
    // Step 5: Module Placement in matrix
    //
    modulePlacement() {
        this.createMatrix();
        this.addFinderPatterns();  // and separators
        this.addAlignmentPatterns();
        this.addTimingPatterns();
        this.addReservedAreas();  // and dark spot
        this.addData();
    }

    createMatrix() {
        this.size = ((this.version - 1) * 4) + 21;
        this.matrix = Array.from({length: this.size}, () => Array(this.size).fill(null));
        this.dataMatrix = Array.from({length: this.size}, () => Array(this.size).fill(null));
    }

    addFinderPatterns() {
        this.placeFinder(0);
        this.placeFinder(1);
        this.placeFinder(2);
    }

    placeFinder(kind) {
        const coords = {0: [0, 0], 1: [0, this.size - 8], 2: [this.size - 8, 0]};
        const pattern = Patterns.finders[kind];
        const [row, col] = coords[kind];
        this.placePattern(pattern, row, col);
    }

    addAlignmentPatterns() {
        const coords = Tables.locations[this.version - 1];

        if (!coords) {
            return;
        }

        const pairs = helper.getPairs(coords);
        const goodPairs = pairs.filter(pair => {
            if (pair[0] <= 8 && pair[1] <= 8) return false;
            if (pair[0] <= 8 && pair[1] >= (this.size - 8)) return false;
            if (pair[0] >= (this.size - 8) && pair[1] <= 8) return false;
            return true;
        });

        goodPairs.forEach(pair => {
            this.placeAlignment(pair[0], pair[1]);
        });
    }

    placeAlignment(row, col) {
        // Convert to corner
        row -= 2;
        col -= 2;
        const pattern = Patterns.alignment;
        this.placePattern(pattern, row, col);
    }

    placePattern(pattern, row, col) {
        pattern.forEach((r, i) => {
            r.forEach((c, j) => {
                this.matrix[row + i][col + j] = pattern[i][j];
            });
        });
    }

    addTimingPatterns() {
        let bw = 1;
        for (let i = 8; i < this.size - 8; i++) {
            const module = bw ? 1 : 0;
            bw = 1 - bw;

            this.matrix[6][i] = module;
            this.matrix[i][6] = module;
        }
    }

    addReservedAreas() {
        // Dark spot
        this.matrix[(4 * this.version) + 9][8] = 1;

        // Format information
        for (let i = 0; i < this.size; i++) {
            if (i <= 8 || i >= this.size - 8) {
                if (this.matrix[8][i] === null) {
                    this.matrix[8][i] = 2;
                }
                if (this.matrix[i][8] === null) {
                    this.matrix[i][8] = 2;
                }
            }
        }

        // Version information
        if (this.version >= 7) {
            for (let i = 0; i < 6; i++) {
                const end = this.size - 9;
                this.matrix[i][end] = 2;
                this.matrix[i][end - 1] = 2;
                this.matrix[i][end - 2] = 2;
                this.matrix[end][i] = 2;
                this.matrix[end - 1][i] = 2;
                this.matrix[end - 2][i] = 2;
            }
        }
    }

    addData() {
        const bits = this.bits;
        let upDirection = true;
        let last = 0;  // 0: vert, 1: hor
        let [i, j] = [this.size - 1, this.size - 1];

        for (const bit of bits) {
            while (this.matrix[i][j] !== null) {
                [i, j, last, upDirection] = this.findNext(i, j, last, upDirection);
            }
            this.matrix[i][j] = parseInt(bit);
            this.dataMatrix[i][j] = parseInt(bit);
        }
    }

    findNext(row, col, last, upDirection) {
        if (upDirection) {
            if (last === 0) {
                col -= 1;
                last = 1;
            } else if (last === 1) {
                row -= 1;
                col += 1;
                last = 0;
            }

            // Reached top, switch downwards
            if (row < 0) {
                row += 1;
                col -= 2;
                last = 0;
                upDirection = false;
            }
        } else {
            if (last === 0) {
                col -= 1;
                last = 1;
            } else if (last === 1) {
                row += 1;
                col += 1;
                last = 0;
            }

            // Reached end
            if (row === this.size) {
                row -= 1;
                col -= 2;
                last = 0;
                upDirection = true;
            }
        }

        if (col === 6) {
            col -= 1;
        }

        return [row, col, last, upDirection];
    }

    //
    // Step 6: Data Masking
    //
    maskData() {
        let scores = [];
        for (let i = 0; i < 8; i++) {
            scores[i] = this.maskAndScore(i);
        }
        let bestMask = scores.indexOf(Math.min(...scores));
        this.matrix = this.mask(bestMask);
        console.log(bestMask)
    }

    maskAndScore(maskNum) {
        let matrix = this.mask(maskNum);
        return helper.score(matrix);
    }

    mask(maskNum) {
        let data = JSON.parse(JSON.stringify(this.dataMatrix));
        switch (maskNum) {
            case 0:
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < data[i].length; j++) {
                        if (data[i][j] === null) continue;
                        if ((i + j) % 2 === 0) {
                            data[i][j] = data[i][j] ^ 1;
                        }
                    }
                }
                break;
            case 1:
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < data[i].length; j++) {
                        if (data[i][j] === null) continue;
                        if (i % 2 === 0) {
                            data[i][j] = data[i][j] ^ 1;
                        }
                    }
                }
                break;
            case 2:
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < data[i].length; j++) {
                        if (data[i][j] === null) continue;
                        if (j % 3 === 0) {
                            data[i][j] = data[i][j] ^ 1;
                        }
                    }
                }
                break;
            case 3:
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < data[i].length; j++) {
                        if (data[i][j] === null) continue;
                        if ((i + j) % 3 === 0) {
                            data[i][j] = data[i][j] ^ 1;
                        }
                    }
                }
                break;
            case 4:
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < data[i].length; j++) {
                        if (data[i][j] === null) continue;
                        if (((Math.floor(i / 2)) + (Math.floor(j / 3))) % 2 === 0) {
                            data[i][j] = data[i][j] ^ 1;
                        }
                    }
                }
                break;
            case 5:
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < data[i].length; j++) {
                        if (data[i][j] === null) continue;
                        if (((i * j) % 2) + ((i * j) % 3) === 0) {
                            data[i][j] = data[i][j] ^ 1;
                        }
                    }
                }
                break;
            case 6:
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < data[i].length; j++) {
                        if (data[i][j] === null) continue;
                        if ((((i * j) % 2) + ((i * j) % 3)) % 2 === 0) {
                            data[i][j] = data[i][j] ^ 1;
                        }
                    }
                }
                break;
            case 7:
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < data[i].length; j++) {
                        if (data[i][j] === null) continue;
                        if ((((i + j) % 2) + ((i * j) % 3)) % 2 === 0) {
                            data[i][j] = data[i][j] ^ 1;
                        }
                    }
                }
                break;
            default:
                throw new Error("Mask Number must be in range(0,8)");
        }

        let matrix = JSON.parse(JSON.stringify(this.matrix));
        for (let i = 0; i < data.length; i++) {
            for (let j = 0; j < data[i].length; j++) {
                if (data[i][j] !== null) {
                    matrix[i][j] = data[i][j];
                }
            }
        }

        matrix = this.addFormatBits(matrix, maskNum);
        return matrix;
    }

    //
    // Step 7: Format and Version Information
    //
    addFormatBits(m, maskNum) {
        const ecLevel = {"L": 0, "M": 1, "Q": 2, "H": 3}[this.level];
        const formatString = Tables.formatStrings[maskNum][ecLevel];

        // Horizontal Format string
        for (let i = 0; i < 15; i++) {
            const num = parseInt(formatString[i], 2);
            if (i <= 6) {
                if (i === 6) {
                    m[8][i + 1] = num;
                } else {
                    m[8][i] = num;
                }
                m[this.size - 1 - i][8] = num;
            } else {
                m[8][this.size - 15 + i] = num;
                if (i <= 8) {
                    m[14 - i + 1][8] = num;
                } else {
                    m[14 - i][8] = num;
                }
            }
        }

        // Version string
        if (this.version >= 7) {
            let versionString = Tables.versionStrings[this.version - 7];
            versionString = versionString.split('').reverse().join('');

            for (let i = 0; i < 6; i++) {
                const end = this.size - 9;
                m[i][end - 2] = parseInt(versionString[3 * i]);
                m[i][end - 1] = parseInt(versionString[(3 * i) + 1]);
                m[i][end] = parseInt(versionString[(3 * i) + 2]);

                m[end - 2][i] = parseInt(versionString[3 * i]);
                m[end - 1][i] = parseInt(versionString[(3 * i) + 1]);
                m[end][i] = parseInt(versionString[(3 * i) + 2]);
            }
        }
        return m;
    }

    finalizeCode() {
        const matrix = Array.from({length: this.size + 8}, () => Array(this.size + 8).fill(0));
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                matrix[i + 4][j + 4] = this.matrix[i][j];
            }
        }
        this.matrix = matrix;
        this.size += 8;
    }

    //
    // Step 8: Create Image Byte Array
    //
    createImage() {
        const mult = 20
        
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d')

        canvas.width = this.size * mult;
        canvas.height = this.size * mult;

        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                ctx.fillStyle = this.matrix[i][j] === 1 ? 'black' : 'white';
                ctx.fillRect(j * mult, i * mult, mult, mult);
            }
        }

        return canvas.toDataURL('image/png')
    }

}
