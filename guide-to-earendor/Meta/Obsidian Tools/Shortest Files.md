
```dataviewjs
const excluded = ['Decks', 'Meta', 'Campaigns'];

const files = dv.pages()
	.filter(p => !excluded.some(folder => p.file.path.includes(folder)))
	.sort(p => p.file.size, 'asc'); // smallest first

dv.table(['File', 'Size (kB)'],
	files.map(p => [p.file.link, (p.file.size / 1024).toFixed(1)]));
```
