
```dataviewjs
const excluded = ['Decks', 'Meta', 'Campaigns'];

const files = dv.pages()
	.filter(p => !excluded.some(folder => p.file.path.includes(folder)))
	.sort(p => p.file.mtime, 'asc'); // oldest modified first

dv.table(['File', 'Last Modified'],
	files.map(p => [p.file.link, p.file.mtime.toLocaleString()]));
```
