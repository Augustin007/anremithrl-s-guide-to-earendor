
```dataview
TABLE file.mtime AS "Last Modified"
FROM ""
WHERE !contains(file.folder, "Meta")
  AND !contains(file.folder, "Decks")
SORT file.mtime DESC
LIMIT 20
```
