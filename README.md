# Ergonomic Automation in Python

Using Python and MySQL to create a Toast Message in Windows.

## Package to install:
<ul>
  <li>pip install mysql.connector</li>
  <li>pip install win10toast</li>
  <li>pip install Pillow</li>
</ul>

## Toaster Content Based on MySQL Data

### Table Content
| id | title | content | path_url | img_path
| --- | --- | --- | --- | --- |


### Table Sequence
| id | content_id | no
| --- | --- | --- |

### Table Sequence Check
| last_run | date
| --- | --- |
