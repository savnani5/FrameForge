// import React, { useState } from 'react';
// import Navbar from './components/Navbar';
// import Footer from './components/Footer';
// import HomePage from './components/HomePage';
// import './App.css';
// import axios from 'axios';

// function FileUpload() {
//   const [file, setFile] = useState(null);

//   const handleFileChange = (event) => {
//     setFile(event.target.files[0]);
//   };

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     if (!file) {
//       alert('Please select a file first!');
//       return;
//     }
//     const formData = new FormData();
//     formData.append('file', file);

//     try {
//       console.log("Uploading file:", file);
//       const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
//         withCredentials: true,
//         headers: {
//             'Content-Type': 'multipart/form/data',
//             'Access-Control-Allow-Credentials': true
//         },
//     });
//       alert(response.data.message);
//     } catch (error) {
//       console.error('Error uploading file:', error);
//       alert('Error uploading file');
//     }
//   };

//   return (
//     <form onSubmit={handleSubmit}>
//       <input type="file" onChange={handleFileChange} />
//       <button type="submit">Upload Video</button>
//     </form>
//   );
// }

// function App() {
//   return (
//     <div className="App">
//       <Navbar />
//       <main>
//         <HomePage />
//         <FileUpload /> {/* Now using the FileUpload component here */}
//       </main>
//       <Footer />
//     </div>
//   );
// }

// export default App;

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

  useEffect(() => {
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        // Use reader.result to display the video preview
        setUploadedVideo(reader.result);
      };
      reader.readAsDataURL(file);
    }
  }, [file]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadedVideo(null);
    setProcessedVideo(null); // Clear previous processed video
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file first!');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    setUploadProgress(0);

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
      // The backend can return the URL to the processed video
      setProcessedVideo(response.data.processedVideoUrl);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} accept="video/*" />
        <button type="submit">Upload Video</button>
      </form>
      {uploadProgress > 0 && uploadProgress < 100 && (
        <progress value={uploadProgress} max="100">{uploadProgress}%</progress>
      )}
      {uploadedVideo && (
        <video controls width="100%" src={uploadedVideo} />
      )}
      {processedVideo && (
        <div>
          <h3>Processed Video</h3>
          <video controls width="100%" src={processedVideo} />
        </div>
      )}
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
