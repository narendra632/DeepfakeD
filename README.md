# Deepfake Detection Django Application

This project focuses on detecting deepfake videos using a combination of ResNext and LSTM networks. Deepfakes are manipulated videos that use artificial intelligence to replace a person's likeness in a video with someone else's. By leveraging machine learning techniques, we aim to identify and flag such deceptive content.

## Requirements:

- **CUDA version >= 10.0 for GPU**: To take advantage of GPU acceleration during model training and inference, ensure that you have CUDA installed on your system. A compatible version is required for optimal performance.

- **GPU Compute Capability > 3.0**: Verify that your GPU meets this requirement. The compute capability determines the features and performance capabilities of your GPU.

All the necessary Python modules are listed in the `requirements.txt` file. Make sure to install them with their specified versions to avoid compatibility issues.

## Running the Application:

Follow these steps to run the deepfake detection application:

1. **Download and Install CUDA version 12.1 (most compatible)**:
   - Download the CUDA toolkit.
   - Install CUDA on your system.

2. **Install Dependencies from `requirements.txt`**:
   - Open a terminal or command prompt.
   - Navigate to the project folder.
   - Run the following command to install the required Python modules:
     ```
     pip install -r requirements.txt
     ```

3. **Open the `Deep_fake_Django` Folder in Visual Studio Code (VS Code)**:
   - Launch VS Code.
   - Open the project folder (`Deep_fake_Django`).

4. **Run the Project**:
   - In the terminal, execute the following command to start the Django development server:
     ```
     python manage.py runserver
     ```

5. **Access the Application**:
   - Open your web browser and go to `http://localhost:8000`.
   - You should see the deepfake detection interface.
   - Adjust the frame selection bar to 40 frames per second (fps).
   - Upload a test video to analyze for deepfake content.
