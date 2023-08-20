<template>
  <div>
    <v-card class="mt-5 mb-12">
      <v-card-title>みんなで画像生成</v-card-title>
      <v-card-text>
        <p>
          皆さんから送信された単語を使用してAIが画像を生成します。<br />下のフォームから単語を送信してください!
        </p>
        <p class="red--text">※英単語のみが入力可能です</p>
      </v-card-text>
    </v-card>
    <v-spacer> </v-spacer>
    <v-row class="mt-12" justify="center">
      <v-col cols="10">
        <v-form>
          <v-text-field label="Word" v-model="word" :rules="rules" outlined placeholder="例）rabbit">
          </v-text-field>
        </v-form>
      </v-col>
    </v-row>
    <v-row>
      <v-col align="center">
        <v-btn color="green" :disabled="!isValid && !isSend" x-large class="font-weight-bold white--text"
          @click="submit()">送信</v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "HomeView",
  data() {
    return {
      isSend: false,
      word: "",
      // 半角英数のみを許可する
      rules: [
        (v) => !!v || "",
        (v) => /^[A-Za-z0-9]*$/.test(v) || "半角英数で入力してください",
      ],
    };
  },
  computed: {
    isValid() {
      if (this.word == "") {
        return false;
      }
      if (this.word.match(/^[A-Za-z0-9]*$/)) {
        return true;
      } else {
        return false;
      }
    },
  },
  methods: {
    reload() {
      this.$router.go({ path: this.$router.currentRoute.path, force: true });
    },
    submit() {
      this.isSend = true;
      axios
        .post(
          `http://localhost:8005/register_word/?word=${this.word}`,
          {
            headers: {
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Headers":
                "Origin, X-Requested-With, Content-Type, Accept",
            },
          }
        )
        .then((res) => {
          console.log(res);
          console.log(res.data);
        })
        .catch((error) => {
          console.log(error);
          alert("単語の送信に失敗しました");
          this.reload();
        });
      this.$router.push("/thanks");
    },
  },
};
</script>
