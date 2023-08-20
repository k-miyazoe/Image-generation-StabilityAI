<template>
  <div>
    <div v-for="image in images" :key="image">
      <img :src="image" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: [],
    };
  },
  mounted() {
    this.fetchImages();
  },
  methods: {
    fetchImages() {
      console.log("fetchImages");
      this.images = [];
      // 同階層のpublicフォルダ内のファイル名を取得する
      const publicFiles = require.context("@/assets", false, /\.png$/);
      console.log(publicFiles.keys());
      for (const file of publicFiles.keys()) {
        this.images.push(file);
      }
    },
  },
};
</script>
