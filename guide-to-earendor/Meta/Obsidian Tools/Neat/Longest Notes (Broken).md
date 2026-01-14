
```dataview
TABLE length(file.content) AS "Characters"
FROM ""
WHERE !contains(file.folder, "Meta")
  AND !contains(file.folder, "Decks")
SORT length(file.content) DESC
LIMIT 20
```
