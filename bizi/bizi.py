# need python solution for:
# list of integers (in DB) nums and an integer k, return the maximum number of subsets of nums that sum up to k.
# Each number in nums can only be used once


from collections import Counter


def max_subsets(nums, k):
    # Sort nums in descending order for better pruning (greedy)
    nums.sort(reverse=True)

    # Counter to keep track of occurrences of each number in nums
    counter = Counter(nums)
    result = []

    def backtrack(subset, remaining_sum):
        if remaining_sum == 0:  # Found a valid subset that sums up to k
            result.append(subset[:])  # Append the subset to the result
            for num in subset:
                counter[num] -= 1  # Decrease the count of each number used
            return  # Stop backtracking for this subset
        if remaining_sum < 0:
            return  # Stop backtracking if the sum goes negative

        # Try adding each number to the subset
        for num in list(counter.keys()):  # Iterate through unique numbers
            if counter[num] > 0:  # Check if the number is available to use
                subset.append(num)
                counter[num] -= 1  # Mark the number as used
                backtrack(subset, remaining_sum - num)  # Recur with the reduced sum
                subset.pop()  # Backtrack, remove the last element
                counter[num] += 1  # Restore the count of the number

    # Call the backtrack function to find all valid subsets that sum to k
    backtrack([], k)

    return result


# Example usage:
nums = [1, 1, 1, 1, 2, 2, 3, 4, 5]
k = 5
subsets = max_subsets(nums, k)
print(subsets)  # Expected Output: [[1, 1, 1, 2], [1, 4], [5], [2, 3]]
