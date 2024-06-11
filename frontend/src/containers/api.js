import axios from "axios";
class api {
  static uploadProfilePicture() {
    var formData = new FormData();

    formData.append("image", "1222");
    formData.append("from", "frontend");

    return postImage(`/user/upload`, formData).then((res) => res);
  }
}

/**
  * 
  
  * @param {FormData} formData 
  * @returns 
  */
let postImage = (endpoint, formData) => {
  const customHeader = {
    headers: {
      // Authorization: `Bearer ${getLocalStorageToken()}`,
      "Content-Type": "multipart/form-data",
    },
  };

  let url = `http://172.20.10.3:5000`;
  return axios
    .post(url, formData, customHeader)
    .then((res) => ({
      status: res.status,
      data: res.data,
      error: null,
    }))
    .catch((err) => {
      return {
        status: err.response ? err.response.status : 0,
        data: {},
        error: err.message,
      };
    });
};
