# FIAP OCR CHALLENGE - PHASE 3
This project is a challenge for build an application that need to expose an interface and process images about fiscal ticket (Cupom fiscal) and extract some data.


## Team
 - Artur Dos Santos Martini: arturmartiniti@gmail.com
 - Fernanda Lima Silva De Carli: decarli.fe@gmail.com
 - Nicholas Costa Pedroso: nicholas.c.pedroso@gmail.com
 - Rogerio Peixoto Birne: rogerio.birne@gmail.com


## Business requirements
- [x] expose interface channel
- [x] process image (OCR) 
- [x] extract data

## Architecture overview 
- [x] API Rest - Flask
- [x] OCR - Tesseract
- [x] Image treatment OpenCV
- [x] Info extract - Regular Expression
- [x] Documentation

## Problem and solution overview
Manually extracting data is a very difficult job when you need to extract some thousands records.
To make it easier, we need to create an application that exposes the interface channel and implements OCR and regular expression to do this automatically.
if you want know more, check references:

[OCR - Optical Character Recognition](https://en.wikipedia.org/wiki/Optical_character_recognition)



## Installation

This project was created using Pycharm Community.

You should install tesseract using the follow command:
```brew install tesseract```

Install all idioms:
```brew install tesseract-lang```

Create your virtual env:
```python3 -m venv venv```

Start Python env:
```source venv/bin/activate```

Update pip:
```pip install --upgrade pip```

Install if necessary the requirements
```pip install -r requirements.txt```

After install any python module run:
```pip freeze > requirements.txt```

## Running

Run main:
```python main.py```


## Using with Postman Collection
[POSTMAN COLLECTION](tools/OCR_collection.json)

## Using with curl
```shell
curl --location --request POST 'http://localhost:5000/upload' \
--form 'file=@"/your-path-image/example_02.jpg"'
```

## Rest Endpoints

**URL** : `/upload`

**Method** : `POST`

**Required** :  `file`

**Form-Data** : `key: file, value: your file`


## Success Response

**Code** : `200 OK`

```json
{
    "company": "47.508.411/0581-54",
    "customer": "228.082.988-62",
    "itens": [
        "001 00000000120289 DET YPE SOOML 6 UN X 2,19 (4,23) 13,14",
        "002 00000000105316 GUARD PAP KIT 23X22 4 UN X 2,09 (2,74) 8,36",
        "003 00000001239774 TORCI PIME MEXI 1006 2 UN X 3.39 (1,81) 6,78",
        "004 00000001819038 PAO SIRIO INTEG 3201 UN X 11,79 (3,16) 11,79",
        "005 00000007094651 AMEND JAP YOKI 5006 1 UN X 10,29 (3,23) 10,29",
        "006 00000004346968 COCA ZERO 2L 1 UN X 8,59 (2,82) 8,59",
        "007 00000001469349 SACOLA VERDE SP 48X5 2 UN X 0,11 (0,08) 0,22",
        "008 00000001469332 SACOLA CINZ 48X55 2 UN X 0,11 (0,08) 0,22"
    ],
    "total": "99.39"
}
```

## Error Responses

**Code** : `400 BAD REQUEST`

**Code** : `500 INTERNAL SERVER ERROR`
