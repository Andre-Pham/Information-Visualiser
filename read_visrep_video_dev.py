# Code to generate text from visual representation video (webcam)

# Import modules
import cv2
from threading import Thread
# Import complimenting scripts
from read_visrep_photo import *
from constants import *

def read_video(output_list):
    '''
    Scans the video feed from the device's webcam for visreps, and if one is
    detected, reads it.
    '''
    # Define video feed from camera
    video = cv2.VideoCapture(0)
    # Define list of successfully read visreps
    read_frames = []

    # Loop to constantly read camera frames (will run on a daemon thread,
    # meaning that it will automatically close when the main thread show_video
    # ends)
    while True:
        # Capture frame by frame
        running_status, frame = video.read()

        # Try scanning a visrep
        try:
            # Define the visrep matrix read from the current frame
            visrep_matrix = read_visrep_photo(frame)
            # Ensure it's a valid visrep by checking if every row in the visrep
            # matrix is the same length as the matrix; equal columns and rows
            if len(visrep_matrix) < 3:
                raise Exception("Invalid visrep reading")
            for row in visrep_matrix:
                if len(row) != len(visrep_matrix):
                    raise Exception("Invalid visrep reading")
            # Validate reading by making sure the same visrep has been scanned
            # twice (to ensure the visrep was read properly)
            if visrep_matrix in read_frames:
                # Return visrep
                #print(visrep_matrix)
                output_list.append(visrep_matrix)
                break
                #return visrep_matrix
                # Reset saved frames
                read_frames = []
            # If this is the first instance of a given visrep
            else:
                # Add it to the read_frames list to validate a second reading
                read_frames.append(visrep_matrix)
        except:
            # No visrep was found in the frame
            print("No visrep found")

def read_visrep_video():
    '''
    Both reads and displays video from the webcam simultaneously, by running
    the video preview on the main thread, and processing the current frame on
    a second thread.
    '''
    output_list = []
    # Define a secondary thread for reading the video
    # https://stackoverflow.com/questions/3221655/python-threading-string-arguments
    video_thread = Thread(target=read_video, args=(output_list,))
    # Set the secondary thread to daemon, so it closes with the main thread
    video_thread.daemon = True
    # Start the secondary thread
    video_thread.start()

    def show_video():
        '''
        Displays the video feed from the device's webcam in a preview window to the
        user.
        '''
        # Define video feed from camera
        video = cv2.VideoCapture(0)

        # Loop to constantly show camera view to user, until they press ESC
        while cv2.waitKey(1) != 27 and video_thread.is_alive():
            # Capture frame by frame
            running_status, frame = video.read()

            # Flip frame to display
            frame = cv2.flip(frame, 1)

            # Display video to user
            cv2.imshow("Video (ESC to quit)", frame)

        # Release resources/device in use (stop using webcam)
        video.release()
        # Close preview window
        cv2.destroyAllWindows()

    # Start the main thread for displaying the video preivew
    show_video()

    # Return the visrep matrix
    return output_list[0]
