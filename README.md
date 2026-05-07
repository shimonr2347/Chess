## Chess Game Viewer
A Python-based graphical user interface (GUI) for visualizing and analyzing chess games stored in PGN (Portable Game Notation) format. This tool translates technical chess notation into human-readable English, making it accessible for both players and non-players alike.

## 🚀 Features
Interactive Game Browser: Automatically scans the splited_pgns directory and organizes games into a hierarchical sidebar for easy selection.

Dynamic Board Rendering: A custom-drawn board using Tkinter Canvas, complete with algebraic coordinates (a-h, 1-8) and high-quality Unicode chess pieces.

Natural Language Descriptions: Translates technical moves into plain English (e.g., "White Knight captures from f3 to d4 - Check!").

Full Playback Control: Navigate through games using Start, End, Next, and Prev controls.

Metadata Inspection: Displays comprehensive PGN header information (Event, Site, Date, Players, Elo, Result) in a dedicated sidebar.

Smart Rule Handling: Explicitly identifies complex chess moves such as:

Kingside and Queenside Castling

Pawn Promotions

En Passant captures

Check and Checkmate states

## 🛠️ Technical Stack
Language: Python 3.x

GUI Framework: Tkinter (Standard Library)

Chess Logic: python-chess

File Management: pathlib for robust cross-platform path handling

## 📋 Prerequisites
Before running the application, ensure you have the python-chess library installed:

``` bash
pip install python-chess
```


## 📂 Project Structure
```
├── asset/                 # Directory containing screenshots
│   └── end.png
│   └── middle.png
│   └── end.png
├── splited_pgns/          # Directory containing PGN files
│   └── Alburt/
│       └── Alburt_1.pgn
│           ...
│       └── Alburt_776.pgn
│   └── capmemel24/  
│       └── capmemel24_1.pgn
|           ...
|       └── capmemel24_9.pgn
├── chess_viewer.py        # Main application script
└── README.md
```

## 🚦 How to Use
Prepare your PGNs: 
Place your .pgn files inside folders within the splited_pgns directory.

Launch the App:

``` bash
python chess_viewer.py
```

Select a Game: 
Use the sidebar on the left to browse and click on a game file.

Analyze: 
Use the control buttons below the board to step through the moves. The right-hand panel will update with the move description and game metadata.

## 💡 Implementation Details: Human-Readable Logic
One of the core features of this simulator is the get_human_move method. Unlike standard viewers that only show coordinates (like e2e4), this tool performs real-time board analysis:

State Peeking: 
It temporarily applies moves to the internal board to detect "Check" or "Checkmate."

Piece Identification: 
It maps coordinate squares back to piece types to provide context.

Action Mapping: 
It differentiates between a simple move and a capture or a special maneuver like castling.

## 🎨 GUI Example
# start of the game:
<img width="1122" height="787" alt="start" src="https://github.com/user-attachments/assets/9307573d-c6b0-4fe1-a2b4-d7f2907b53f5" />

# middle of the game:
<img width="1122" height="788" alt="middle" src="https://github.com/user-attachments/assets/480bafbe-d9e0-48c5-9223-8440d774ffbe" />

# end of the game:
<img width="1122" height="787" alt="end" src="https://github.com/user-attachments/assets/82b490a7-fdf5-45c7-9550-2005e74b7bc8" />



