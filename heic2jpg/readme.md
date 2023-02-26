# Introduction

Simple tool to convert iPhone HEIC images to JPG format.

## Usage

Define HEIC files directory in main.py file:
```
directory = '/mnt/c/Users/<user>/Downloads/DCIM/'
```
Note: in our case folder "DCIM" contains multiple subfolders with HEIC files.

Execute main.py file:
```python
python main.py
```	


## Dependencies

- Was developed using Python 3.11.0
- Mogrify from ImageMagick package

## Logs

Events are logged in heic2jpg.log file.

## Development

```
export PIPENV_NO_INHERIT=true
pipenv shell
```