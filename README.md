# Hand Cricket AI using Computer Vision

A real-time Hand Cricket game built using **Python, OpenCV, and MediaPipe** that allows players to play cricket against the computer using hand gestures detected through a webcam.

The game uses Computer Vision to recognize finger counts and converts them into cricket runs, creating an interactive touch-free gaming experience.

---

## Features

- Real-time hand tracking using MediaPipe
- Finger gesture recognition (0–6 runs)
- Toss system (Odd/Even)
- Choose Batting or Bowling
- AI-controlled computer opponent
- Automatic score tracking
- Target-based second innings
- Restart game option
- Interactive webcam-based gameplay

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Computer Vision
- Hand Landmark Detection

---

## How to Play

### Start the Game
Press:

```text
S
```

to start the game.

### Toss

Choose:

```text
O = Odd
E = Even
```

Show your hand when the countdown ends.

### Batting / Bowling

If you win the toss:

```text
B = Bat
W = Bowl
```

### Supported Gestures

| Fingers Shown | Runs |
|--------------|------|
| Fist | 0 |
| Index Finger | 1 |
| Index + Middle | 2 |
| Three Fingers | 3 |
| Four Fingers | 4 |
| Five Fingers | 5 |
| Thumb Only | 6 |

### Getting Out

If both player and computer show the same number:

```text
OUT
```

### Winning

- First innings sets the target.
- Second innings chases the target.
- Team with the higher score wins.

---

## Project Structure

```text
hand-cricket-ai/
│
├── main.py
├── README.md
└── requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/hand-cricket-ai.git
cd hand-cricket-ai
```

Install dependencies:

```bash
pip install opencv-python mediapipe
```

Run the project:

```bash
python main.py
```

---

## Future Improvements

- Multiplayer mode
- Difficulty levels
- Sound effects
- Better gesture recognition
- Match statistics
- Graphical User Interface (GUI)
- Online leaderboard

---

## Demo

Add screenshots, GIFs, or a demo video here.

---

## Author

**Sundar B**

Computer Science Engineering Student at SRM Institute of Science and Technology (SRMIST)

Interested in:
- Software Development
- Artificial Intelligence
- Computer Vision
- Problem Solving

GitHub: https://github.com/SundarB07
