def slinding_window(arr, k):
    n =len(arr)
    if k >= n: 
        return -1
    
    max_sum = sum_window = sum(arr[:k])
    
    for i in range (n-k):
        sum_window = sum_window - arr[i] + arr[i +k]
        max_sum = max(max_sum, sum_window)
    return max_sum