def minimumAbsoluteDifference(arr):
	## sort the array in ascending order
	arr.sort()
	## initialize a starting difference value
	min_diff = abs(arr[0] - arr[1])
	## loop through the elements to find the min difference
	for i in range(len(arr)-1):
		curr_diff = abs(arr[i] - arr[i+1])
		if curr_diff < min_diff:
			min_diff = curr_diff
	return min_diff
  
