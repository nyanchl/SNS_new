<template>
  <v-container grid-list-md>
    <v-flex xs12 sm8 lg4 md5>
      <v-layout row wrap align-center justify-center fill-height>
        <v-card class="login-card">
          <v-card-title>
          <span class="headline">Hoge</span>
          </v-card-title>
          <p>debug</p>
          <v-card-text>
            <v-layout row fill-height justify-center align-center v-if="loading">
                <v-progress-circular
                :size="50"
                color="primary"
                indeterminate
                />
            </v-layout>


            <v-form v-else ref="form" v-model="valid" lazy-validation>
                <v-container>

                <v-text-field v-model="credentials.username" :counter="70" label="Eメールアドレス" maxlength="70" required/>

                <v-text-field type="password" v-model="credentials.password" :counter="20" label="パスワード" maxlength="20" required/>

                </v-container>
                <v-btn class="pink white--text" :disabled="!valid" @click="login">Login</v-btn>

            </v-form>


            </v-card-text>
        </v-card>
      </v-layout>
    </v-flex>
  </v-container>
</template>

<script>
export default {
    name: 'Login',
    data: () => ({
        credentials: {},
        valid:true,
        loading:false
    }),
    methods: {
        login() {

        }
    }
}
</script>

<style scoped>
.title-color {
  color: green;
}
</style>