# Orquesta - an open source automation tool for remote terminal operations

As its name implies (which means orchestra in English), this tool work as a director who indicates instructions to musicians (terminals in this context) and each piece is inside a sheet music (a script here). Well, really working with terminals is less complex, because it's possible to decompose all we require into four basic operations: select network nodes, open connections, send commands and close connections. It's the main idea behind the design.

## Motivation

As usual, improvement opportunities arise when tools to work efficiently are missing and fortunately it's something that occurs very often. Keeping this in mind, I was needing a software that meets the following:

> Open Source, looking for collaboration and customization

> Provide a simple scripting interface to automate boring tasks

> Always save the logs, don't know when you'll need it (a golden rule, at least in my job)


## Usage

### Configuration

Create a file with extension `.cfg` in the directory `cfg` that contain for example:

```ini
[DEFAULT]
port = 22
protocol = ssh

[foobar]
ip = 127.0.0.1

[foo]
ip = 127.0.0.1
port = 2222 
```

The `DEFAULT` section must contain the `port` (TCP port) and `protocol` (ssh or telnet) used by default in the nodes defined within the file. Then a section for each node and its respective  `ip` address (version 4 or 6).

### Initial window

When the program starts it shows a window like the following, here we select the logs directory, the project name and a group of nodes or terminals defined in the previous `cfg` file.

![orquesta_init](https://user-images.githubusercontent.com/9748291/27972441-6625fb9e-6324-11e7-87b8-60432b4d4d9c.png)


### Main window

Mainly consist in a text editor where we write the script and a list of nodes (terminals) that can be selected by clicking it or using the `sel` command (see next section).    

![orquesta_main](https://user-images.githubusercontent.com/9748291/27972445-69e9c756-6324-11e7-8cd8-8a1d98a1e5ce.png)

### Available commands

command | parameters | description |
--- | --- | --- |
`open`  | none | open selected nodes |
`sel`   | list of node names or `all` | select the nodes in the list | 
`set`   |  var value | create the variable $var |
`send`  | text | send text to selected terminals|
`gsend` | text | perform substitution of local variables  |
`inv`   |  none | invert selection |
`view`  |  none | view selected nodes |
`close`    |  none  | close selected nodes |
`mainsel`  | list of node names |  avoid the selection of nodes different to the provided in the list  |
`#` | text | comment |


### Keyboard shortcuts

shortcut | action |
--- | --- |
 <kbd>F1</kbd> | Execute current line and move to the next (if no errors) |
 <kbd>F2</kbd> | Execute current line |
 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>S</kbd> | Select all terminals |
 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>D</kbd> | Unselect all terminals |
 <kbd>Ctrl</kbd> + <kbd>I</kbd> | Invert current selection |
 <kbd>Ctrl</kbd> + <kbd>O</kbd> | Open selected terminals |
 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>C</kbd> | Close selected terminals |
 <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd> | Open local terminal in current logs path \* |
 <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>F</kbd> | Open file explorer in current logs path |
 <kbd>Ctrl</kbd> + <kbd>E</kbd> | Exit application |
 <kbd>Ctrl</kbd> + <kbd>S</kbd> | Save script |
 <kbd>Ctrl</kbd> + <kbd>N</kbd> | New project |

\* It try to open `git-bash` as a first option, else `cmd` by default.

### Using templates

Each script could be saved as a template. Just select the menu, write a name and the script would be available the next time the application starts.

## Installation

### Windows installer

**[Download here](https://github.com/ej-f/orquesta/releases)**

### For developers

```bash
git clone https://github.com/ej-f/orquesta.git
cd orquesta
pip install -r requirements.txt
cd orquesta
python orquesta.py
```

#### Requirements

* Python 3.4
  * PyQt4 v4.11.3 -> GUI and process
  * pywin32 219 -> windows automation
  * cx_Freeze 4.3.4 -> to create a standalone executable if is needed
* Qt Designer 4.8.6 -> GUI
* Kitty 0.60 -> client (already included in this repository)

## Todo

### Improvements

* Documentation
* Testing 
* Clean up code base, redefine models and data structures

### Nice to have features

* Expect-like functionality
* Commands highlight
* Select elements using glob patterns
* Cross platform compatibility 
* Automatic script execution
