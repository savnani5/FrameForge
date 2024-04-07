import cv2

class SupplyWriter:
    def __init__(self, input_video, output_video, opt_thres, rgb_input=True):
        reader = cv2.VideoCapture(input_video)
        fps = reader.get(cv2.CAP_PROP_FPS)
        width = int(reader.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        reader.release()
        
        # Choose MP4V as a common codec for .mp4 files
        # Make sure your output_video filename ends with '.mp4'
        fourcc = cv2.VideoWriter_fourcc(*"MP4V")

        self.writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        self.rgb_input = rgb_input
        self.opt_thres = opt_thres

    def run(self, images, scores, boxes):
        # Text variables
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        thickness = 2  # Adjusted for better visibility
        font_scale = 1  # Adjusted for better visibility

        for image, score, box in zip(images, scores, boxes):
            # print(score)
            if self.rgb_input:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if box is not None:
                label = "real" if score > self.opt_thres else "fake"
                x1, y1, x2, y2 = box
                color = (0, 255, 0) if label == "real" else (0, 0, 255)  # BGR
                cv2.putText(
                    image,
                    f"{label}: {score:.2f}",
                    (x1, y1 - 10),
                    font_face,
                    font_scale,
                    color,
                    thickness,
                    cv2.LINE_AA,
                )
                # draw box over face
                cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
            self.writer.write(image)
        self.writer.release()

