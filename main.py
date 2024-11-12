import cv2
import csv
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone
from datetime import datetime

# Initialize video capture and hand detector
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

# Color scheme (professional blue theme)
COLORS = {
    'primary': (82, 109, 130),     # Dark blue
    'secondary': (221, 230, 237),  # Light blue
    'accent': (255, 159, 67),      # Orange
    'correct': (76, 175, 80),      # Green
    'wrong': (244, 67, 54),        # Red
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}

class MCQ:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])
        self.userAns = None
        self.startTime = None
        self.timeSpent = 0
        self.isCorrect = False
        self.explanation = data[6] if len(data) > 6 else "No explanation provided."

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), COLORS['accent'][::-1], cv2.FILLED)
                return True
        return False

class QuizStats:
    def __init__(self):
        self.correct_answers = 0
        self.total_time = 0
        self.question_times = []
        self.performance_history = []
        
    def update(self, mcq):
        self.question_times.append(mcq.timeSpent)
        if mcq.userAns == mcq.answer:
            self.correct_answers += 1
        self.performance_history.append(mcq.userAns == mcq.answer)

    def get_average_time(self):
        return sum(self.question_times) / len(self.question_times) if self.question_times else 0

    def get_accuracy(self):
        return (self.correct_answers / len(self.performance_history)) * 100 if self.performance_history else 0

def draw_modern_button(img, text, position, size=(200, 50), color=COLORS['primary']):
    x, y = position
    w, h = size
    overlay = img.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), color[::-1], cv2.FILLED)
    cv2.addWeighted(overlay, 0.8, img, 0.2, 0, img)
    cv2.putText(img, text, (x + 10, y + h//2 + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS['black'][::-1], 2)
    return [x, y, x + w, y + h]

def save_quiz_results(stats, mcqList):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"quiz_results_{timestamp}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Question', 'Your Answer', 'Correct Answer', 'Time Spent (s)', 'Result'])
        for mcq in mcqList:
            writer.writerow([
                mcq.question,
                mcq.userAns if mcq.userAns else 'Skipped',
                mcq.answer,
                round(mcq.timeSpent, 2),
                'Correct' if mcq.userAns == mcq.answer else 'Incorrect'
            ])
        writer.writerow(['Summary Statistics'])
        writer.writerow(['Total Questions', len(mcqList)])
        writer.writerow(['Correct Answers', stats.correct_answers])
        writer.writerow(['Accuracy', f"{stats.get_accuracy():.2f}%"])
        writer.writerow(['Average Time per Question', f"{stats.get_average_time():.2f}s"])

pathCSV = "Mcqs.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

mcqList = [MCQ(q) for q in dataAll]
qNo = 0
qTotal = len(dataAll)
timer = 20  
stats = QuizStats()
show_explanation = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (1280, 720), COLORS['primary'][::-1], -1)
    cv2.addWeighted(overlay, 0.1, img, 0.9, 0, img)
    
    hands, img = detector.findHands(img, flipType=False)

    if qNo < qTotal:
        mcq = mcqList[qNo]
        
        if mcq.startTime is None:
            mcq.startTime = time.time()
        
        timeRemaining = timer - int(time.time() - mcq.startTime)
        if timeRemaining <= 0:
            mcq.timeSpent = timer
            stats.update(mcq)
            qNo += 1
            continue

        cv2.putText(img, f"Question {qNo + 1}/{qTotal}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS['primary'][::-1], 2)
        
        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, 
                                     colorR=COLORS['primary'], offset=50, border=5)
        
        choice_boxes = []
        for i, choice in enumerate([mcq.choice1, mcq.choice2, mcq.choice3, mcq.choice4]):
            x = 100 if i % 2 == 0 else 400
            y = 250 if i < 2 else 400
            img, bbox = cvzone.putTextRect(img, choice, [x, y], 2, 2, 
                                         colorR=COLORS['black'], offset=50, border=5)
            choice_boxes.append(bbox)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8][:2]
            result = detector.findDistance(lmList[8][:2], lmList[12][:2])
            
            if result[0] < 35:
                if mcq.update(cursor, choice_boxes):
                    mcq.timeSpent = timer - timeRemaining
                    stats.update(mcq)
                    qNo += 1
                    time.sleep(0.3)

        skip_bbox = draw_modern_button(img, "Skip", (1100, 600), color=COLORS['accent'])
        
        if hands and skip_bbox[0] < cursor[0] < skip_bbox[2] and skip_bbox[1] < cursor[1] < skip_bbox[3]:
            mcq.timeSpent = timer - timeRemaining
            stats.update(mcq)
            qNo += 1
            time.sleep(0.3)

    else:
        score = stats.get_accuracy()
        avg_time = stats.get_average_time()
        
        cv2.rectangle(img, (300, 100), (980, 600), COLORS['primary'][::-1], cv2.FILLED)
        cv2.rectangle(img, (320, 120), (960, 580), COLORS['black'][::-1], cv2.FILLED)
        
        texts = [
            ("Quiz Completed!", 400, 180),
            (f"Final Score: {score:.1f}%", 400, 250),
            (f"Average Time: {avg_time:.1f}s per question", 400, 320),
            (f"Correct Answers: {stats.correct_answers}/{qTotal}", 400, 390)
        ]
        
        for text, x, y in texts:
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                       COLORS['primary'][::-1], 2)

        save_bbox = draw_modern_button(img, "Save Results", (400, 500))
        reset_bbox = draw_modern_button(img, "Reset Quiz", (700, 500))
        
        if hands:
            cursor = hands[0]['lmList'][8][:2]
            if save_bbox[0] < cursor[0] < save_bbox[2] and save_bbox[1] < cursor[1] < save_bbox[3]:
                save_quiz_results(stats, mcqList)
                cv2.putText(img, "Results Saved!", (1100, 650), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS['correct'], 2)
                time.sleep(1)

            if reset_bbox[0] < cursor[0] < reset_bbox[2] and reset_bbox[1] < cursor[1] < reset_bbox[3]:
                qNo = 0
                stats = QuizStats()
                time.sleep(1)

    cv2.imshow("Quiz App", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
