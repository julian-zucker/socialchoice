Running on the dog vote datasets is giving me this result:

```

Pairwise: ['57', '20', '65', '40', '37', '35', '70', '43', '45', '28', '34', '52', '54', '27', '24', '25', '51', '44', '48', '74', '56', '38', '72', '26', '68', '69']
Rankings: ['65', '57', '20', '40', '43', '37', '70', '35', '52', '34', '45', '28', '25', '27', '54', '24', '51', '44', '48', '38', '56', '74', '72', '26', '68', '69']

```

As you can see, 65 now leads the group. Recalling a previous data analysis, which found that taking only the first 20 votes lead to a different outcome, I hypothesize that upsampling the rankings, so that one ranking is put in the pool for each pairwise vote, instead of one ranking per voter, will level out the outcomes.

```
Closer...
Pairwise: ['57', '20', '65', '40', '37', '35', '70', '43', '45', '28', '34', '52', '54', '27', '24', '25', '51', '44', '48', '74', '56', '38', '72', '26', '68', '69']
Rankings: ['57', '20', '40', '65', '35', '37', '70', '43', '45', '34', '28', '52', '54', '25', '27', '24', '51', '44', '48', '56', '38', '72', '26', '74', '68', '69']

```