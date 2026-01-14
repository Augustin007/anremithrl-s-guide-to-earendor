
Files with no links coming into them
```dataview
TABLE file.outlinks
FROM ""
WHERE length(file.inlinks) = 0
  AND !contains(file.folder, "Meta")
  AND !contains(file.folder, "Decks")
SORT file.name ASC
```
