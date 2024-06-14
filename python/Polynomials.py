from Tables import Tables


class Polynomial:
    # i in represents a exponent in x^[len - i - 1]
    def __init__(self, c):
        self.coef = c

    def gf256_mult_with(self, poly2):
        # Input -> Polynomial obj in alpha notation
        # Output -> Polynomial obj in alpha nontation
        p1 = self.coef
        p2 = poly2.coef
        p1, p2 = make_same_length(p1, p2)
        p3 = [None] * (2 * (len(p1) - 1) + 1)
        
        for i, c1 in enumerate(p1):
            if c1 is None:
                continue
            for j, c2 in enumerate(p2):
                if c2 is None:
                    continue
                
                e1 = len(p1) - i - 1
                e2 = len(p2) - j - 1
                e3 = e1 + e2
                
                if p3[len(p3) - e3 - 1] is None:
                    c3 = (c1 + c2) % 255
                    p3[len(p3) - e3 - 1] = c3
                
                else:
                    int1 = Tables.antilog[p3[len(p3) - e3 - 1]]
                    c3 = (c1 + c2) % 255
                    int2 = Tables.antilog[c3]
                    int3 = int1 ^ int2
                    p3[len(p3) - e3 - 1] = Tables.log[int3]
        
        res = []
        for n in p3:
            if n is None:
                continue
            res.append(n)
    
        return Polynomial(res)

    def gf256_divide_by(self, poly):
        # Input -> 1 Polynomial obj in alpha notation
        # Output -> coefficients of remainder of division in int notation
        dividend = self.coef
        divisor = poly.coef
        k = len(dividend) - len(divisor) + 1

        for _ in range(k):
            dividend = divide_once(dividend, divisor.copy())

        return to_int(dividend)


def make_same_length(p1, p2):
    if len(p1) == len(p2):
        return p1, p2
    diff = len(p1) - len(p2)
    if diff > 0:
        p2 = ([None] * diff) + p2
    else:
        diff = -diff
        p1 = ([None] * diff) + p1
    return p1, p2


def generate_n_generator_polynomials(n):
    poly1 = Polynomial([0, 0])
    ps = [poly1]
    for i in range(2, n + 1):
        poly2 = Polynomial([0, i-1])
        new = ps[len(ps) - 1].gf256_mult_with(poly2)
        ps.append(Polynomial(new))
    return ps


def divide_once(dividend, divisor):
    # input -> 2 coefficient lists | alpha notation
    # output -> coef of remainder from one division in alpha notation
    assert len(divisor) <= len(dividend)

    factor = dividend[0]
    if factor is None:
        return dividend[1:]

    # Multiply factor and convert to int
    for i, c in enumerate(divisor):
        if c is None:
            divisor[i] = 0
        else:
            e  = c + factor
            e = e % 255
            divisor[i] = Tables.antilog[e]

    dividend = to_int(dividend)

    # Expand divisor coeff
    divisor += [0] * (len(dividend) - len(divisor))

    # XOR result with message polynomial
    for i, c in enumerate(dividend):
        d1 = divisor[i]
        d2 = c
        dividend[i] = d1 ^ d2

    # Discard first (will always be 0)
    dividend = dividend[1:]

    dividend = to_exp(dividend)

    return dividend


def to_int(coef):
    for i, c in enumerate(coef):
        if c is None:
            coef[i] = 0
            continue
        coef[i] = Tables.antilog[c]
    return coef


def to_exp(coef):
    for i, c in enumerate(coef):
        coef[i] = Tables.log[c]
    return coef


if __name__ == "__main__":
    res = [None]
    for p in generate_n_generator_polynomials(30):
        res.append(p.coef)
    print(res)
    
    