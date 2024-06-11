import axios from "axios";
class api {
  static uploadProfilePicture(name, url) {
    var formData = new FormData();

    formData.append("username", name);
    formData.append("jpg", url);

    return postImage(`/frontendrequestreg`, formData).then((res) => res);
  }

  static waitProcess() {
    return getInfo(`/frontendcheckreg`).then((res) => res);
  }
  static loginFace(url) {
    var formData = new FormData();

    formData.append("jpg", url);

    return postImage(`/frontendrequestlog`, formData).then((res) => res);
    // waiting: true => detect face success
    // waiting: false => detect face error
  }

  static waitLoginProcess() {
    return getInfo(`/frontendchecklog`).then((res) => res);
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

  let url = `http://172.20.10.3:8080${endpoint}`;
  return axios
    .post(url, formData, customHeader)
    .then((res) => {
      return {
        status: res.status,
        data: res.data,
        error: null,
      };
    })
    .catch((err) => {
      return {
        status: err.response ? err.response.status : 0,
        data: {},
        error: err.message,
      };
    });
};

let getInfo = (endpoint) => {
  const customHeader = {
    headers: {
      // Authorization: `Bearer ${getLocalStorageToken()}`,
      "Content-Type": "multipart/form-data",
    },
  };

  let url = `http://172.20.10.3:8080${endpoint}`;
  return axios
    .get(url, customHeader)
    .then((res) => {
      console.log(res.data); // This logs the response to the console
      return {
        status: res.status,
        data: res.data,
        error: null,
      };
    })
    .catch((err) => {
      return {
        status: err.response ? err.response.status : 0,
        data: {},
        error: err.message,
      };
    });
};

export { api };
