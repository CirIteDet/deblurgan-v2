arr = [1,2,3,2,1,2,3,2,1,2,3,2,1,2,3,1,1,1,2,2,2,3,3,3]
start = 0
end = len(arr) - 1
left = len(arr) // 2
right = left + 1
while start <= left or right <= end:
    if start > left:
        arr[start], arr[right] = arr[right], arr[start]
        left += 1
        right += 1
    elif right > end:
        arr[left], arr[end] = arr[end], arr[left]
        right -= 1
        left -= 1

    if arr[start] == 1:
        start += 1
    elif arr[start] == 2:
        arr[left], arr[start] = arr[start], arr[left]
        left -= 1
    elif arr[start] == 3:
        arr[end], arr[start] = arr[start], arr[end]
        end -= 1

print(arr)