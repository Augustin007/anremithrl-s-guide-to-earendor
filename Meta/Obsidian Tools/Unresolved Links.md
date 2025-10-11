
```dataview
TABLE without id 
out AS "Uncreated files", file.link as "Origin"
FLATTEN file.outlinks as out
WHERE !(out.file) 
  AND !contains(meta(out).path, "/")
  AND !contains(file.folder, "Meta")
  AND !contains(file.folder, "Decks")
  AND !contains(file.name, "Session")
SORT out ASC
````

