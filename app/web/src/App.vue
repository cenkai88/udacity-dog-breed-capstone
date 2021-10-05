<template>
  <div>
    <Header />
    <div class="row">
      <div
        class="upload-container"
        id="drop-area"
        :style="isHovered ? 'border-color: #71c0e5; border-width: 3px;' : ''"
      >
        <div v-if="!imagePreviewUrl" class="upload-box">
          <div class="upload-box-text">
            <div>
              <img
                style="width: 100px; margin-bottom: 20px"
                src="./assets/dog.svg"
              />
            </div>
            <div>Drag image into the box to see if it's a 🐶!</div>
            <div style="margin-top: 12px">
              <input
                type="file"
                accept="image/png,image/jpeg,image/jpg"
                @change="getUpload"
              />
            </div>
          </div>
        </div>
        <div v-else class="image-preview">
          <div class="image-preview-image">
            <img
              :src="imagePreviewUrl"
              style="max-width: 100%; max-height: 59vh"
            />
          </div>
        </div>
        <div v-if="isLoading" class="image-preview-loading">
          <img src="./assets/loading.svg" class="loading-icon" />
        </div>
      </div>
    </div>
    <div v-if="result" class="result">
      {{ result }}
      <img @click="reset" class="reset-icon" src="./assets/reset.svg" />
    </div>
  </div>
</template>

<script>
const axios = require("axios");

import Header from "./components/Header.vue";

export default {
  name: "App",
  components: {
    Header,
  },
  data() {
    return {
      result: "",
      isLoading: false,
      isHovered: false,
      imagePreviewUrl: undefined,
      imageLoader: undefined,
    };
  },
  methods: {
    reset() {
      this.result = "";
      this.isLoading = false;
      this.imagePreviewUrl = undefined;
    },
    onDrop(e) {
      e.stopPropagation();
      e.preventDefault();
      this.isHovered = false;
      const file = e.dataTransfer.files[0];
      this.imageLoader.readAsDataURL(file);
      this.submit(file);
    },
    async getUpload({ target }) {
      const file = target.files[0];
      this.imageLoader.readAsDataURL(file);
      this.submit(file);
    },
    async submit(file) {
      const params = new FormData();
      params.append("file", file, file.name);
      this.isLoading = true;
      const { data } = await axios.post(
        `http://localhost:3000/image/dog_breed_classification/v1`,
        params,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      this.result = data.result;
      this.isLoading = false;
    },
  },
  async mounted() {
    const dropbox = document.getElementById("drop-area");
    dropbox.addEventListener("drop", this.onDrop.bind(this), false);
    dropbox.addEventListener("dragleave", (e) => {
      e.stopPropagation();
      e.preventDefault();
      this.isHovered = false;
    });
    dropbox.addEventListener("dragenter", (e) => {
      e.stopPropagation();
      e.preventDefault();
      this.isHovered = true;
    });
    dropbox.addEventListener("dragover", (e) => {
      e.stopPropagation();
      e.preventDefault();
      this.isHovered = true;
    });

    this.imageLoader = new FileReader();
    this.imageLoader.onload = (e) => {
      console.log(e);
      this.imagePreviewUrl = this.imageLoader.result;
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body {
  margin: 0;
}
.row {
  display: flex;
  justify-content: space-evenly;
  margin: 24px 0;
}
.upload-container {
  margin-top: 40px;
  border: 2px dashed #cccccc;
  width: 42vw;
  height: 60vh;
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
}
.upload-box-text {
  position: absolute;
  font-weight: 500;
  font-size: 18px;
  bottom: 30%;
  left: 20vw;
  transform: translateX(-50%);
  text-align: center;
}
.result {
  position: absolute;
  top: calc(60vh + 140px);
  font-weight: 600;
  width: 100%;
  line-height: 24px;
}
.image-preview-loading {
  position: absolute;
  background: rgba(0, 0, 0, 0.5);
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.loading-icon {
  width: 32px;
  height: 32px;
  animation: rotate 2s infinite forwards;
  top: calc(50% - 16px);
  position: absolute;
}
.reset-icon {
  width: 24px;
  height: 24px;
  line-height: 24px;
  margin-left: 12px;
  transform: translateY(5px);
  cursor: pointer;
}
@keyframes rotate {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
