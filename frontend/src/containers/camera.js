import React, { useState, useEffect, useRef } from "react";
import Webcam from "react-webcam";
import Box from "@mui/material/Box";
import { useNMLab } from "./hooks/useNMLab";
import Button from "@mui/material/Button";
import DoneOutlineIcon from "@mui/icons-material/DoneOutline";
import ReplayIcon from "@mui/icons-material/Replay";
//https://codesandbox.io/p/sandbox/react-webcam-demo-wrecn?file=%2Fsrc%2FCamera.js%3A2%2C25

const videoConstraints = {
  width: 860,
  facingMode: "environment",
};

const Camera = () => {
  const webcamRef = useRef(null);
  const [status, setStatus] = React.useState(false);
  const { saveFace, setSaveFace, sendphoto, countDown, setUrl, url } = useNMLab();

  useEffect(() => {
    if (countDown == 0) {
      capturePhoto();
    }
  }, [countDown]);

  const capturePhoto = React.useCallback(async () => {
    //generate a photo based on base64
    //remove "data:image/png;base64," from head and decode to get the image
    // https://stackoverflow.com/questions/69167751/how-to-properly-send-an-image-from-react-to-java
    //https://stackoverflow.com/questions/58806971/how-can-i-take-a-picture-in-react-web-application-not-native
    const imageSrc = webcamRef.current.getScreenshot();
    setUrl(imageSrc);
    setStatus(true);
  }, [webcamRef]);

  const onUserMedia = (e) => {
    console.log(e);
  };
  return (
    <Box
      display="flex"
      height="89vh"
      width={"100%"}
      alignItems="center"
      flexDirection="row"
      justifyContent="center"
      flexWrap="wrap"
    >
      {!status ? (
        <>
          <Box width={"72%"} display="flex" justifyContent="center">
            <Webcam
              ref={webcamRef}
              audio={false}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              onUserMedia={onUserMedia}
              style={{ borderRadius: "40px" }}
            />
          </Box>
          <Box width={"28%"} fontSize={"100px"}>
            <button onClick={capturePhoto}>Capture</button>
            {countDown}
            {/* <button onClick={() => start()}>Refresh</button> */}
          </Box>
        </>
      ) : (
        url && (
          <>
            <Box width={"68%"}>
              <img src={url} alt="Screenshot" style={{ borderRadius: "40px" }} />
            </Box>
            <Box
              width={"32%"}
              display="flex"
              flexDirection="column"
              justifyContent="center"
              alignItems="center"
            >
              <Box padding="20px" fontSize={"40px"} sx={{ mt: "30px" }}>
                請確認您的臉在照片中
              </Box>
              <Box
                height="30vh"
                alignItems="center"
                flexDirection="row"
                sx={{ mt: "20px" }}
              >
                <Button
                  variant="contained"
                  style={{ fontSize: "25px", borderRadius: "10px" }}
                  onClick={() => {
                    sendphoto(url);
                  }}
                  endIcon={<DoneOutlineIcon />}
                >
                  確認
                </Button>

                <Button
                  variant="contained"
                  style={{ fontSize: "25px", borderRadius: "10px", marginLeft: "20px" }}
                  onClick={() => {
                    setSaveFace("retry");
                    setStatus(false);
                  }}
                  endIcon={<ReplayIcon />}
                >
                  重試
                </Button>
              </Box>
            </Box>
          </>
        )
      )}
    </Box>
  );
};

export default Camera;
/*export const uploadImage = (fileObj) => dispatch => {

  return fetch(url, {
    method: 'POST',
    headers: {
      'Accept': 'image/jpeg'
    },
    body: fileObj
  })
    .then((response) => response.json())
    .then(function (response) {
      if (response.status === 'success') {
        console.log(response);
        // ... Show feedback
        return response
      } else {
        // ... Show feedback
      }
    })
    .catch((error) => {
      console.error(error)
    });
}
*/
/*var params = { 
    Bucket: 'bucketName', 
    Key: Date.now() + '.jpg',
    ContentType: 'image/jpeg',
    Body: event.body,
    ACL: "public-read"
  };
  return uploading = new Promise(function (resolve, reject) {
    return s3.upload(params, function (err, data) {
      if(err) {
        state.uploadError = err
        return reject({
          error: err,
          status: 'error',
          message: 'something went wrong'
        })
      }
      state.uploadData = data
      state.fileLocation = data.Location
      state.status = "success"
      state.message = "File has been uploaded to the fileLocation"
      return resolve(data)
    });
  }) */
