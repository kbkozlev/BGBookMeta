# BGBookMeta

BGBookMeta е инструмент за скрейпване на уебстраници за метаданни на книги написани на български език.

Към момента, инструментът извлича данни от следните уебсайтове:

* https://biblioman.chitanka.info/
* ~~https://helikon.bg/~~ понякога е блокиран от cloudflare
* https://knizhen-pazar.net/
* https://www.orangecenter.bg/knizharnitsa

### Пример
 ![Example1](https://i.imgur.com/RzLQ1nl.png)
 
### Изтегляне и Стартиране
Изтеглете последната версия на програмата от <a href="https://github.com/kbkozlev/BGBookMeta/releases/latest/download/BGBookMeta.exe">тук</a>, или използвайте командния ред за изтегляне на изходния код:

#### Уиндоус
```bash
curl -LO https://github.com/kbkozlev/BGBookMeta/archive/refs/heads/master.zip
tar -xf master.zip
cd BGBookMeta-master
pip install -r requirements.txt
python main.py
```

#### Линукс
```bash
wget https://github.com/kbkozlev/BGBookMeta/archive/refs/heads/master.zip
unzip master.zip
cd BGBookMeta-master
pip install -r requirements.txt
python3 main.py
```
### Лиценз

Този проект е лицензиран под MIT лиценз - вижте [LICENSE](LICENSE) файла за повече детайли.

### Подкрепете ме 
<div>
<a href="https://www.buymeacoffee.com/kbkozlev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</div>
