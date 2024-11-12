# Hand-Gesture Controlled Quiz App

This project is a hand-gesture controlled quiz application developed with OpenCV and Python. It allows users to interact with multiple-choice questions using hand gestures, leveraging a webcam and OpenCV's hand tracking module. The app tracks the user's answers, calculates accuracy, and saves results in a CSV file. Ideal for hands-free quiz applications and educational tools!

## Features
- **Hand Gesture Interaction**: Control the quiz with hand gestures, allowing touch-free question answering.
- **Modern UI**: Uses a professional blue color scheme for a clean and modern interface.
- **Quiz Statistics**: Track time spent per question, accuracy, and overall performance.
- **Result Export**: Saves quiz results and performance summary to a CSV file.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Mayankgupta1754/AI-Project-computer-vision-.git
    cd hand-gesture-quiz-app
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
   Ensure you have the following packages installed:
   - OpenCV
   - NumPy
   - CVZone
3. Prepare a CSV file (`Mcqs.csv`) in the same directory containing the quiz questions in this format:
    ```
    Question,Choice1,Choice2,Choice3,Choice4,Answer,Explanation
    ```
   Example:
    ```csv
    What is 2+2?,2,3,4,5,3,Correct answer is 4.
    ```

## Usage
1. Run the script:
    ```bash
    python quiz_app.py
    ```
2. **Interface Controls**:
   - **Answering Questions**: Hover over the answer box and hold the index finger near the thumb to select.
   - **Skip Question**: Hover over the "Skip" button at the bottom right.
   - **Save Results**: Save quiz results by hovering over the "Save Results" button on the summary screen.
   - **Reset Quiz**: Start over by hovering over the "Reset Quiz" button on the summary screen.
3. **Exiting**: Press `q` to quit the application.

## File Structure
- **quiz_app.py**: Main script to run the application.
- **Mcqs.csv**: CSV file containing the questions and answers.
- **quiz_results_TIMESTAMP.csv**: Generated quiz results after completing the quiz.

## Customization
- **Color Scheme**: Modify the `COLORS` dictionary in `quiz_app.py` to adjust theme colors.
- **Quiz Timer**: Change the `timer` variable for setting the time limit per question.

## Future Improvements
- **Feedback on Incorrect Answers**: Display explanations for incorrect answers after each question.
- **Enhanced Hand Detection**: Experiment with different `detectionCon` values to improve hand gesture detection accuracy.
- **Multiplayer Mode**: Add support for multiple users or teams competing in real time.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Credits
Built with 💙 by [Mayank Gupta](https://github.com/Mayankgupta1754).
