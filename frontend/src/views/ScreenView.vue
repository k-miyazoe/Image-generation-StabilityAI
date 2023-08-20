<template>
  <div>
    <v-row>
      <v-col v-for="(image, index) in images" :key="index" class="d-flex child-flex" cols="6">
        <v-row align-content="center">
          <v-col cols="8">
            <v-img :src="image" aspect-ratio="1" class="grey lighten-2">
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
                </v-row>
              </template>
            </v-img>
          </v-col>
          <v-col class="mt-8" cols="3">
            <h1>{{ words[index] }}</h1>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-btn class="mt-12" @click="getImagesAndWords">test</v-btn>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "ScreenView",
  data() {
    return {
      images: [],
      words: [],
      interval: 30000, // リクエストを送る間隔(ms)
    };
  },
  mounted() {
    // 30秒に一度リクエストを送る
    setInterval(() => {
      console.log("satart generate image");
      this.getImagesAndWords();
    }, this.interval);
  },
  methods: {
    getImagesAndWords() {
      axios
        .post("http://localhost:8005/generate_image/", {
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers":
              "Origin, X-Requested-With, Content-Type, Accept",
          },
        })
        .then((response) => {
          var res_data = JSON.parse(response.data);
          if (res_data["words"] == "error") {
            console.log("error");
            console.log(res_data["word_count"]);
            return;
          } else {
            this.words.push(res_data["words"]);
            this.images.push(
              `${res_data["file_path"].replace("./images/", "")}`
            );
            axios.delete(
              "http://localhost:8005/delete_all_words/",
              {
                headers: {
                  "Access-Control-Allow-Origin": "*",
                  "Access-Control-Allow-Headers":
                    "Origin, X-Requested-With, Content-Type, Accept",
                },
              }
            );
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>
