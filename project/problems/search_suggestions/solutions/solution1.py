def solve(params):
    # params: dict with 'products' and 'searchWord'
    products = sorted(params.get('products', []))
    word = params.get('searchWord', '')
    ans = []
    for i in range(1, len(word)+1):
        prefix = word[:i]
        matches = [p for p in products if p.startswith(prefix)][:3]
        ans.append(matches)
    return ans
