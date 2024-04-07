import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './components/HomePage';
import './App.css';
import axios from 'axios';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedVideo, setUploadedVideo] = useState(null);
  const [processedVideo, setProcessedVideo] = useState(null);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setUploadedVideo(reader.result);
      };
      reader.readAsDataURL(file);
    }
  }, [file]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadedVideo(null);
    setProcessedVideo(null); // Reset previous processed video
  };

  const pollForProcessedVideo = (filename) => {
    // Start processing indicator
    setProcessing(true);
  
    // Poll every 2 seconds to check if the processed video is ready
    const intervalId = setInterval(async () => {
      try {
        // Use the filename returned from the upload response
        const response = await axios.get(`http://127.0.0.1:5000/uploads/${filename}`);
        
        // If the file is found, clear the interval and set the processed video URL
        if (response.status === 200) {
          clearInterval(intervalId);
          setProcessing(false);
          setProcessedVideo(response.config.url);
        }
      } catch (error) {
        if (error.response && error.response.status === 404) {
          console.log('Processing, waiting for the video...');
        } else {
          // If an error other than 404 occurs, stop polling and log the error
          clearInterval(intervalId);
          setProcessing(false);
          console.error('Error during processing:', error);
        }
      }
    }, 2000);
  };
  
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file first!');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);

    setUploadProgress(0); // Reset progress at the start
    setProcessing(false); // Reset processing at the start

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        withCredentials: true,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        },
      });

      if (response.status === 200 && response.data.filename) {
        // Use the filename from the response to poll for the processed video
        setUploadProgress(100); // Upload is complete
        pollForProcessedVideo(response.data.filename);
      } else {
        // Handle the case where the filename is not returned
        alert('Error: filename not returned from server.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    }
  };

  return (
    <div className="video-upload-container">
      <div className="video-section">
        <h2>Input Video Preview</h2>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} accept="video/*" />
          <button type="submit">Upload Video</button>
        </form>
        {uploadProgress > 0 && uploadProgress < 100 && (
          <progress value={uploadProgress} max="100">{uploadProgress}%</progress>
        )}
        {uploadedVideo && <video controls src={uploadedVideo} />}
        {processing && <div>Processing the video...</div>}
      </div>
      <div className="video-section">
        <h2>Processed Video</h2>
        {processedVideo ? (
          <video controls src={processedVideo} key={processedVideo}/>) : (
          <div>Processed video will appear here</div>
        )}
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <Navbar />
      <main>
        <HomePage />
        <FileUpload /> {/* FileUpload now handles video upload and display */}
      </main>
      <Footer />
    </div>
  );
}

export default App;
