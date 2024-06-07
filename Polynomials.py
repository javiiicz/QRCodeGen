from Tables import Tables


class Polynomial:
    # i in represents a exponent in x^[len - i - 1]
    def __init__(self, c):
        self.coef = c

    def gf256_mult_with(self, poly2):
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
    
        return res


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
        
if __name__ == "__main__":
    res = [None]
    for p in generate_n_generator_polynomials(30):
        res.append(p.coef)
    print(res)
    
    