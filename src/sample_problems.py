sample_problems = [
    # Easy Problems
    (1, "Two Sum", "Easy", "Array", ["Hash Table"], "https://leetcode.com/problems/two-sum/", "High", []),
    (2, "Add Two Numbers", "Easy", "Linked List", ["Iteration"], "https://leetcode.com/problems/add-two-numbers/", "High", []),
    (3, "Valid Parentheses", "Easy", "Stack", ["Stack"], "https://leetcode.com/problems/valid-parentheses/", "High", []),
    (4, "Merge Two Sorted Lists", "Easy", "Linked List", ["Two Pointers"], "https://leetcode.com/problems/merge-two-sorted-lists/", "High", []),
    (6, "Palindrome Linked List", "Easy", "Linked List", ["Fast and Slow Pointers"], "https://leetcode.com/problems/palindrome-linked-list/", "Medium", []),
    (7, "Reverse Linked List", "Easy", "Linked List", ["Iteration"], "https://leetcode.com/problems/reverse-linked-list/", "High", []),
    (9, "Climbing Stairs", "Easy", "Dynamic Programming", ["Recursion"], "https://leetcode.com/problems/climbing-stairs/", "High", []),
    (11, "Container With Most Water", "Medium", "Array", ["Two Pointers"], "https://leetcode.com/problems/container-with-most-water/", "High", [1]),
    (20, "Binary Search", "Easy", "Binary Search", ["Binary Search"], "https://leetcode.com/problems/binary-search/", "High", []),
    (23, "Linked List Cycle", "Easy", "Linked List", ["Two Pointers"], "https://leetcode.com/problems/linked-list-cycle/", "High", [5, 7]),
    (24, "Maximum Depth of Binary Tree", "Easy", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/maximum-depth-of-binary-tree/", "High", []),  # Placeholder
    (25, "Symmetric Tree", "Easy", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/symmetric-tree/", "Medium", [24]),
    (27, "Maximum Depth of Binary Tree", "Easy", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/maximum-depth-of-binary-tree/", "High", [24]),
    (111, "Palindrome Number", "Easy", "Math", ["Math"], "https://leetcode.com/problems/palindrome-number/", "High", []),
    (118, "Sum of Left Leaves", "Easy", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/sum-of-left-leaves/", "High", [24]),
    (145, "Same Tree", "Easy", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/same-tree/", "High", [24]),

    (151, "Maximum Depth of N-ary Tree", "Easy", "Tree", ["Recursion"], "https://leetcode.com/problems/maximum-depth-of-n-ary-tree/", "Medium", [24]),
    (152, "Number of 1 Bits", "Easy", "Bit Manipulation", ["Bit Manipulation"], "https://leetcode.com/problems/number-of-1-bits/", "Medium", []),
    (153, "Counting Bits", "Easy", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/counting-bits/", "Medium", []),
    (154, "Minimum Number of Days to Make m Bouquets", "Easy", "Binary Search", ["Binary Search"], "https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/", "Medium", [20]),
    (155, "Min Stack", "Easy", "Stack", ["Stack"], "https://leetcode.com/problems/min-stack/", "High", [3]),
    (156, "Binary Tree Level Order Traversal II", "Easy", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/binary-tree-level-order-traversal-ii/", "Medium", [24]),
    (157, "Read N Characters Given Read4", "Easy", "String", ["String Manipulation"], "https://leetcode.com/problems/read-n-characters-given-read4/", "Medium", [15]),
    (158, "Read N Characters Given Read4 II - Call multiple times", "Easy", "String", ["String Manipulation"], "https://leetcode.com/problems/read-n-characters-given-read4-ii-call-multiple-times/", "Medium", [157]),
    (159, "Longest Substring with At Most Two Distinct Characters", "Easy", "String", ["Sliding Window"], "https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/", "Medium", [15]),
    (160, "Intersection of Two Linked Lists", "Easy", "Linked List", ["Two Pointers"], "https://leetcode.com/problems/intersection-of-two-linked-lists/", "High", [5, 7]),
    (161, "One Edit Distance", "Easy", "String", ["String Manipulation"], "https://leetcode.com/problems/one-edit-distance/", "Medium", [15]),
    (162, "Find Peak Element II", "Easy", "Binary Search", ["Binary Search"], "https://leetcode.com/problems/find-peak-element-ii/", "Medium", [20]),
    (163, "Missing Ranges", "Easy", "Array", ["Array Manipulation"], "https://leetcode.com/problems/missing-ranges/", "Medium", [101]),
    (164, "Maximum Gap", "Easy", "Array", ["Sorting"], "https://leetcode.com/problems/maximum-gap/", "Medium", [1]),
    (165, "Compare Version Numbers", "Easy", "String", ["String Manipulation"], "https://leetcode.com/problems/compare-version-numbers/", "Medium", [15]),
    (166, "Fraction to Recurring Decimal", "Easy", "Math", ["Math"], "https://leetcode.com/problems/fraction-to-recurring-decimal/", "Medium", [3]),
    (167, "Two Sum II - Input array is sorted", "Easy", "Array", ["Two Pointers"], "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/", "High", [1]),
    (168, "Excel Sheet Column Title", "Easy", "Math", ["Math"], "https://leetcode.com/problems/excel-sheet-column-title/", "Medium", [3]),
    (169, "Majority Element II", "Easy", "Hash Table", ["Hash Table"], "https://leetcode.com/problems/majority-element-ii/", "Medium", [11]),
    (170, "Two Sum III - Data structure design", "Easy", "Hash Table", ["Hash Table"], "https://leetcode.com/problems/two-sum-iii-data-structure-design/", "Medium", [11]),
    (171, "Excel Sheet Column Number", "Easy", "Math", ["Math"], "https://leetcode.com/problems/excel-sheet-column-number/", "Medium", [3]),
    (172, "Factorial Trailing Zeroes", "Easy", "Math", ["Math"], "https://leetcode.com/problems/factorial-trailing-zeroes/", "Medium", [3]),
    (174, "Dungeon Game", "Easy", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/dungeon-game/", "Medium", [8]),
    (175, "Combine Two Tables", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/combine-two-tables/", "Medium", []),
    (176, "Second Highest Salary", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/second-highest-salary/", "Medium", [175]),
    (177, "Nth Highest Salary", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/nth-highest-salary/", "Medium", [175]),
    (178, "Rank Scores", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/rank-scores/", "Medium", [175]),
    (179, "Largest Number", "Easy", "Greedy", ["Greedy"], "https://leetcode.com/problems/largest-number/", "Medium", [15]),
    (180, "Consecutive Numbers", "Easy", "Array", ["Array Manipulation"], "https://leetcode.com/problems/consecutive-numbers/", "Medium", [101]),
    (181, "Employees Earning More Than Their Managers", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/employees-earning-more-than-their-managers/", "Medium", [175]),
    (182, "Duplicate Emails", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/duplicate-emails/", "Medium", [175]),
    (183, "Customers Who Never Order", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/customers-who-never-order/", "Medium", [175]),
    (184, "Department Highest Salary", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/department-highest-salary/", "Medium", [175]),
    (185, "Department Top Three Salaries", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/department-top-three-salaries/", "Medium", [175]),
    (186, "Reverse Words in a String II", "Easy", "String", ["String Manipulation"], "https://leetcode.com/problems/reverse-words-in-a-string-ii/", "Medium", [15]),
    (187, "Repeated DNA Sequences", "Easy", "Hash Table", ["Hash Table"], "https://leetcode.com/problems/repeated-dna-sequences/", "Medium", [11]),
    (188, "Best Time to Buy and Sell Stock IV", "Easy", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/", "High", []),
    (189, "Rotate Array", "Easy", "Array", ["Array Manipulation"], "https://leetcode.com/problems/rotate-array/", "Medium", [1]),
    (190, "Reverse Bits", "Easy", "Bit Manipulation", ["Bit Manipulation"], "https://leetcode.com/problems/reverse-bits/", "Medium", [152]),
    (191, "Number of 1 Bits", "Easy", "Bit Manipulation", ["Bit Manipulation"], "https://leetcode.com/problems/number-of-1-bits/", "Medium", [152]),
    (192, "Word Frequency", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/word-frequency/", "Medium", [175]),
    (193, "Valid Phone Numbers", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/valid-phone-numbers/", "Medium", [175]),
    (194, "Transpose File", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/transpose-file/", "Medium", [175]),
    (195, "Tenth Line", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/tenth-line/", "Medium", [175]),
    (196, "Delete Duplicate Emails", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/delete-duplicate-emails/", "Medium", [175]),
    (197, "Rising Temperature", "Easy", "Database", ["SQL"], "https://leetcode.com/problems/rising-temperature/", "Medium", [175]),
    (198, "House Robber", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/house-robber/", "High", [8]),
    (199, "Binary Tree Right Side View", "Medium", "Binary Tree", ["Breadth-First Search"], "https://leetcode.com/problems/binary-tree-right-side-view/", "Medium", [24]),
    (200, "Number of Islands", "Medium", "Graph", ["Depth-First Search"], "https://leetcode.com/problems/number-of-islands/", "High", []),
    
    # Medium Problems
    (2, "Best Time to Buy and Sell Stock", "Easy", "Array", ["Dynamic Programming"], "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/", "High", []),
    (5, "Remove Nth Node From End of List", "Medium", "Linked List", ["Two Pointers"], "https://leetcode.com/problems/remove-nth-node-from-end-of-list/", "High", [4]),
    (8, "Maximum Subarray", "Medium", "Array", ["Dynamic Programming"], "https://leetcode.com/problems/maximum-subarray/", "High", [2]),
    (10, "Coin Change", "Medium", "Dynamic Programming", ["Recursion", "Memoization"], "https://leetcode.com/problems/coin-change/", "High", [9]),
    (12, "Group Anagrams", "Medium", "Hash Table", ["Hash Table"], "https://leetcode.com/problems/group-anagrams/", "Medium", [11]),
    (13, "Top K Frequent Elements", "Medium", "Hash Table", ["Heap"], "https://leetcode.com/problems/top-k-frequent-elements/", "High", [12]),
    (14, "Product of Array Except Self", "Medium", "Array", ["Prefix Product"], "https://leetcode.com/problems/product-of-array-except-self/", "High", [1]),
    (15, "Longest Substring Without Repeating Characters", "Medium", "String", ["Sliding Window"], "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "High", [1]),
    (16, "Longest Palindromic Substring", "Medium", "String", ["Dynamic Programming"], "https://leetcode.com/problems/longest-palindromic-substring/", "High", [15]),
    (17, "Minimum Window Substring", "Medium", "String", ["Sliding Window"], "https://leetcode.com/problems/minimum-window-substring/", "Medium", [15]),
    (18, "Implement Trie (Prefix Tree)", "Medium", "Trie", ["Trie"], "https://leetcode.com/problems/implement-trie-prefix-tree/", "Medium", []),
    (19, "Word Search", "Medium", "Backtracking", ["Backtracking"], "https://leetcode.com/problems/word-search/", "Medium", [18]),
    (21, "Course Schedule", "Medium", "Graph", ["Topological Sort"], "https://leetcode.com/problems/course-schedule/", "High", [20]),
    (22, "Find the Duplicate Number", "Medium", "Array", ["Two Pointers"], "https://leetcode.com/problems/find-the-duplicate-number/", "High", [1]),
    (26, "Binary Tree Level Order Traversal", "Medium", "Binary Tree", ["Breadth-First Search"], "https://leetcode.com/problems/binary-tree-level-order-traversal/", "High", [24]),
    (28, "Validate Binary Search Tree", "Medium", "Binary Search Tree", ["Recursion"], "https://leetcode.com/problems/validate-binary-search-tree/", "High", [24]),
    (29, "Lowest Common Ancestor of a Binary Search Tree", "Medium", "Binary Search Tree", ["Recursion"], "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/", "High", [28]),
    (30, "Binary Tree Zigzag Level Order Traversal", "Medium", "Binary Tree", ["Breadth-First Search"], "https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/", "Medium", [26]),
    (33, "Minimum Path Sum", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/minimum-path-sum/", "Medium", [8]),
    (34, "Unique Paths", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/unique-paths/", "High", [9]),
    (36, "Palindrome Partitioning", "Medium", "Backtracking", ["Backtracking"], "https://leetcode.com/problems/palindrome-partitioning/", "Medium", [16]),
    (37, "Combination Sum", "Medium", "Backtracking", ["Backtracking"], "https://leetcode.com/problems/combination-sum/", "High", [18]),
    (38, "Subsets", "Medium", "Backtracking", ["Backtracking"], "https://leetcode.com/problems/subsets/", "High", [7]),
    (39, "Permutations", "Medium", "Backtracking", ["Backtracking"], "https://leetcode.com/problems/permutations/", "High", [7]),
    (44, "Longest Consecutive Sequence", "Medium", "Union-Find", ["Union-Find"], "https://leetcode.com/problems/longest-consecutive-sequence/", "Medium", [1]),
    (45, "Kth Largest Element in an Array", "Medium", "Heap", ["Heap"], "https://leetcode.com/problems/kth-largest-element-in-an-array/", "High", [1]),
    (46, "Find All Anagrams in a String", "Medium", "String", ["Sliding Window"], "https://leetcode.com/problems/find-all-anagrams-in-a-string/", "Medium", [15]),
    (47, "Word Ladder", "Medium", "Graph", ["Breadth-First Search"], "https://leetcode.com/problems/word-ladder/", "High", [18]),
    (49, "Longest Increasing Subsequence", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/longest-increasing-subsequence/", "High", [8]),
    (51, "Decode Ways", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/decode-ways/", "Medium", [9]),
    (52, "House Robber", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/house-robber/", "High", [8]),
    (53, "House Robber II", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/house-robber-ii/", "Medium", [52]),
    (55, "Longest Palindromic Subsequence", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/longest-palindromic-subsequence/", "Medium", [16]),
    (56, "Minimum Size Subarray Sum", "Medium", "Array", ["Sliding Window", "Binary Search"], "https://leetcode.com/problems/minimum-size-subarray-sum/", "Medium", [15]),
    (57, "Insert Interval", "Medium", "Array", ["Two Pointers"], "https://leetcode.com/problems/insert-interval/", "Medium", [1,20]),
    (58, "Merge Intervals", "Medium", "Array", ["Sorting"], "https://leetcode.com/problems/merge-intervals/", "Medium", [59]),
    (59, "Meeting Rooms", "Easy", "Array", ["Sorting"], "https://leetcode.com/problems/meeting-rooms/", "Medium", []),
    (63, "Word Break", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/word-break/", "High", [51]),
    (64, "Unique Binary Search Trees", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/unique-binary-search-trees/", "Medium", [28]),
    (65, "Unique Binary Search Trees II", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/unique-binary-search-trees-ii/", "Medium", [64]),
    (66, "Reorder List", "Medium", "Linked List", ["Two Pointers"], "https://leetcode.com/problems/reorder-list/", "Medium", [5]),
    (67, "LRU Cache", "Medium", "Hash Table", ["Hash Table", "Design"], "https://leetcode.com/problems/lru-cache/", "High", [11]),
    (68, "Design Twitter", "Medium", "Heap", ["Heap", "Design"], "https://leetcode.com/problems/design-twitter/", "High", [13]),
    (71, "Binary Tree Right Side View", "Medium", "Binary Tree", ["Breadth-First Search"], "https://leetcode.com/problems/binary-tree-right-side-view/", "Medium", [24]),
    (72, "Path Sum", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/path-sum/", "High", [24]),
    (73, "Flatten Binary Tree to Linked List", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/flatten-binary-tree-to-linked-list/", "Medium", [24]),
    (74, "Count Complete Tree Nodes", "Medium", "Binary Tree", ["Binary Search"], "https://leetcode.com/problems/count-complete-tree-nodes/", "Medium", [24]),
    (75, "Kth Smallest Element in a BST", "Medium", "Binary Search Tree", ["Binary Search"], "https://leetcode.com/problems/kth-smallest-element-in-a-bst/", "Medium", [28]),
    (77, "Sum Root to Leaf Numbers", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/sum-root-to-leaf-numbers/", "Medium", [24]),
    (78, "Populating Next Right Pointers in Each Node", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/populating-next-right-pointers-in-each-node/", "Medium", [24]),
    (80, "All Nodes Distance K in Binary Tree", "Medium", "Binary Tree", ["Breadth-First Search"], "https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/", "Medium", [24]),
    (81, "Path Sum II", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/path-sum-ii/", "Medium", [24]),
    (82, "Subarray Sum Equals K", "Medium", "Hash Table", ["Hash Table"], "https://leetcode.com/problems/subarray-sum-equals-k/", "High", [8]),
    (83, "House Robber III", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/house-robber-iii/", "Medium", [52]),
    (85, "Basic Calculator II", "Medium", "Math", ["Iteration"], "https://leetcode.com/problems/basic-calculator-ii/", "Medium", [3]),
    (86, "Implement Stack using Queues", "Easy", "Stack", ["Queue"], "https://leetcode.com/problems/implement-stack-using-queues/", "High", [3]),
    (87, "Binary Search Tree Iterator", "Medium", "Binary Search Tree", ["Iteration"], "https://leetcode.com/problems/binary-search-tree-iterator/", "Medium", [28]),
    (88, "Maximum Product Subarray", "Medium", "Array", ["Dynamic Programming"], "https://leetcode.com/problems/maximum-product-subarray/", "High", [8]),
    (89, "Number of Connected Components in an Undirected Graph", "Medium", "Union-Find", ["Union-Find"], "https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/", "Medium", [44]),
    (90, "Spiral Matrix", "Medium", "Array", ["Matrix Traversal"], "https://leetcode.com/problems/spiral-matrix/", "Medium", [1]),
    (91, "Spiral Matrix II", "Medium", "Array", ["Matrix Traversal"], "https://leetcode.com/problems/spiral-matrix-ii/", "Medium", [90]),
    (92, "Set Matrix Zeroes", "Medium", "Array", ["Matrix Traversal"], "https://leetcode.com/problems/set-matrix-zeroes/", "Medium", [91]),
    (93, "Rotate Image", "Medium", "Array", ["Matrix Traversal"], "https://leetcode.com/problems/rotate-image/", "Medium", [90]),
    (95, "Restore IP Addresses", "Medium", "Backtracking", ["Backtracking"], "https://leetcode.com/problems/restore-ip-addresses/", "Medium", [19]),
    (97, "Binary Tree Pruning", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/binary-tree-pruning/", "Medium", [24]),
    (98, "Sum of Two Integers", "Medium", "Math", ["Bit Manipulation"], "https://leetcode.com/problems/sum-of-two-integers/", "Medium", []),
    (99, "Single Number", "Medium", "Hash Table", ["Hash Table"], "https://leetcode.com/problems/single-number/", "High", [11]),
    (100, "Majority Element", "Medium", "Hash Table", ["Hash Table"], "https://leetcode.com/problems/majority-element/", "High", [11]),
    (101, "Missing Number", "Medium", "Array", ["Bit Manipulation", "Mathematics"], "https://leetcode.com/problems/missing-number/", "High", []),
    (102, "Find All Numbers Disappeared in an Array", "Medium", "Array", ["Hash Table", "Array Manipulation"], "https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/", "Medium", [101]),
    (103, "Find Peak Element", "Medium", "Binary Search", ["Binary Search"], "https://leetcode.com/problems/find-peak-element/", "Medium", [20]),
    (104, "Search in Rotated Sorted Array", "Medium", "Binary Search", ["Binary Search"], "https://leetcode.com/problems/search-in-rotated-sorted-array/", "Medium", [20]),
    (105, "Find First and Last Position of Element in Sorted Array", "Medium", "Binary Search", ["Binary Search"], "https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/", "Medium", [20]),
    (106, "Search a 2D Matrix", "Medium", "Binary Search", ["Binary Search"], "https://leetcode.com/problems/search-a-2d-matrix/", "Medium", [20]),
    (107, "Find Minimum in Rotated Sorted Array", "Medium", "Binary Search", ["Binary Search"], "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/", "Medium", [20]),
    (110, "Rotate List", "Medium", "Linked List", ["Two Pointers"], "https://leetcode.com/problems/rotate-list/", "Medium", [5]),
    (114, "Flatten Nested List Iterator", "Medium", "Tree", ["Iteration"], "https://leetcode.com/problems/flatten-nested-list-iterator/", "Medium", [5]),
    (116, "Populating Next Right Pointers in Each Node II", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/", "Medium", [24]),
    (119, "Binary Tree Tilt", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/binary-tree-tilt/", "Medium", [24]),
    (122, "Game of Life", "Medium", "Array", ["Simulation", "Array Manipulation"], "https://leetcode.com/problems/game-of-life/", "Medium", [1]),
    (125, "Minimum Domino Rotations For Equal Row", "Medium", "Greedy", ["Greedy", "Array Manipulation"], "https://leetcode.com/problems/minimum-domino-rotations-for-equal-row/", "Medium", [1]),
    (126, "Wiggle Subsequence", "Medium", "Dynamic Programming", ["Dynamic Programming", "Greedy"], "https://leetcode.com/problems/wiggle-subsequence/", "Medium", [8]),
    (127, "Longest Arithmetic Subsequence", "Medium", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/longest-arithmetic-subsequence/", "Medium", [8]),
    (129, "Longest Substring with At Most Two Distinct Characters", "Medium", "String", ["Sliding Window"], "https://leetcode.com/problems/longest-substring-with-at-most-two-distinct-characters/", "Medium", [15]),
    (131, "Minimum Number of Arrows to Burst Balloons", "Medium", "Greedy", ["Greedy", "Array Manipulation"], "https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/", "Medium", [1]),
    (133, "Clone Graph", "Medium", "Graph", ["Depth-First Search", "Breadth-First Search"], "https://leetcode.com/problems/clone-graph/", "Medium", [20]),
    (134, "Gas Station", "Medium", "Greedy", ["Greedy"], "https://leetcode.com/problems/gas-station/", "Medium", [1]),
    (135, "Jump Game", "High", "Dynamic Programming", ["Greedy"], "https://leetcode.com/problems/jump-game/", "High", [8]),
    (136, "Jump Game II", "Medium", "Dynamic Programming", ["Greedy"], "https://leetcode.com/problems/jump-game-ii/", "Medium", [135]),
    (138, "Copy List with Random Pointer", "Medium", "Linked List", ["Hash Table", "Linked List"], "https://leetcode.com/problems/copy-list-with-random-pointer/", "Medium", [5]),
    (139, "Longest Harmonious Subsequence", "Medium", "Array", ["Hash Table"], "https://leetcode.com/problems/longest-harmonious-subsequence/", "Medium", [1]),
    (140, "Longest Univalue Path", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/longest-univalue-path/", "Medium", [24]),
    (141, "Linked List Cycle II", "Medium", "Linked List", ["Two Pointers"], "https://leetcode.com/problems/linked-list-cycle-ii/", "Medium", [5]),
    (143, "Reorder Data in Log Files", "Medium", "String", ["Sorting", "String Manipulation"], "https://leetcode.com/problems/reorder-data-in-log-files/", "Medium", [15]),
    (144, "Find All Duplicates in an Array", "Medium", "Array", ["Hash Table", "Array Manipulation"], "https://leetcode.com/problems/find-all-duplicates-in-an-array/", "Medium", [1]),
    (145, "Same Tree", "Easy", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/same-tree/", "High", [24]),
    (146, "Binary Tree Right Side View II", "Medium", "Binary Tree", ["Breadth-First Search"], "https://leetcode.com/problems/binary-tree-right-side-view-ii/", "Medium", [24]),
    
    # Hard Problems (10)
    (41, "Merge k Sorted Lists", "Hard", "Heap", ["Heap"], "https://leetcode.com/problems/merge-k-sorted-lists/", "High", [4, 13]),
    (42, "Find Median from Data Stream", "Hard", "Heap", ["Heap"], "https://leetcode.com/problems/find-median-from-data-stream/", "High", [13]),
    (108, "Find Minimum in Rotated Sorted Array II", "Hard", "Binary Search", ["Binary Search"], "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/", "High", [107]),
    (109, "First Missing Positive", "Hard", "Array", ["Array Manipulation"], "https://leetcode.com/problems/first-missing-positive/", "High", [101]),
    (115, "Distinct Subsequences", "Hard", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/distinct-subsequences/", "High", [9]),
    (116, "Populating Next Right Pointers in Each Node II", "Medium", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/", "Medium", [24]),
    (117, "Populating Next Right Pointers in Each Node III", "Hard", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/populating-next-right-pointers-in-each-node-iii/", "High", [24]),
    (120, "Binary Tree Cameras", "Hard", "Binary Tree", ["Greedy", "Recursion"], "https://leetcode.com/problems/binary-tree-cameras/", "High", [24]),
    (123, "Text Justification", "Hard", "String", ["Greedy", "String Manipulation"], "https://leetcode.com/problems/text-justification/", "High", [15]),
    (124, "Binary Tree Maximum Path Sum II", "Hard", "Binary Tree", ["Recursion"], "https://leetcode.com/problems/binary-tree-maximum-path-sum-ii/", "High", [24]),
   # (130, "Substring with Concatenation of All Words", "Hard", "Hash Table", ["Sliding Window", "Hash Table"], "https://leetcode.com/problems/substring-with-concatenation-of-all-words/", "High", [15]),
   # (132, "Palindrome Partitioning II", "Hard", "Dynamic Programming", ["Dynamic Programming"], "https://leetcode.com/problems/palindrome-partitioning-ii/", "High", [36]),
   # (142, "Linked List Cycle III", "Hard", "Linked List", ["Two Pointers"], "https://leetcode.com/problems/linked-list-cycle-iii/", "High", [5]),
   # (143, "Reorder Data in Log Files", "Medium", "String", ["Sorting", "String Manipulation"], "https://leetcode.com/problems/reorder-data-in-log-files/", "Medium", [15]),
   # (148, "Largest Rectangle in Histogram", "Hard", "Stack", ["Stack"], "https://leetcode.com/problems/largest-rectangle-in-histogram/", "High", [3]),
   # (150, "Basic Calculator III", "Hard", "Math", ["Recursion", "Expression Parsing"], "https://leetcode.com/problems/basic-calculator-iii/", "High", [3]),
   # (137, "Minimum Number of K Consecutive Bit Flips", "Hard", "Greedy", ["Greedy", "Sliding Window"], "https://leetcode.com/problems/minimum-number-of-k-consecutive-bit-flips/", "High", [15]),
   # (135, "Jump Game", "High", "Dynamic Programming", ["Greedy"], "https://leetcode.com/problems/jump-game/", "High", [8]),
]
