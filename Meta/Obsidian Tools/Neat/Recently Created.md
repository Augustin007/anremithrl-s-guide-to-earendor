
```dataview
TABLE file.ctime AS "Created"
FROM ""
WHERE !contains(file.folder, "Meta")
  AND !contains(file.folder, "Decks")
SORT file.ctime DESC
LIMIT 20
```
