<template>
  <div class="orders">
    <!--bootstrap navigation bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="/orders">Sneha's Code-Test</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarColor01"
          aria-controls="navbarColor01"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
    </nav>
    <!--linking font awesome for icons -->
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
    />
    <form class="d-flex mt-4" @submit="onSubmit">
      <!--search input -->
      <input
        class="form-control me-sm-2"
        id="search-text"
        type="text"
        v-model="filter.filt"
        placeholder="Search"
      />
      <!--search button-->
      <button
        class="btn btn-dark my-2 my-sm-0"
        id="search-button"
        type="submit"
      >
        <i class="fa fa-search" style="font-size: 24px"></i> Search
      </button>
    </form>
    <br /><br />
    <div class="date-create ml-5">
      <b>Creation Date</b>
      <br />
      <form class="d-flex mt-4" @change="onChange">
        <!--filter for created date -->
        <label for="start">Start Date : &nbsp;</label>
        <input type="date" id="start" name="start" v-model="date.startdate" />
        <label for="end">&nbsp;&nbsp;End Date :&nbsp;</label>
        <input type="date" id="end" name="end" v-model="date.enddate" />
      </form>
    </div>
    <center>
      <table class="table bg-light mt-5" id="order-table">
        <thead>
          <tr>
            <th scope="col">Order Name</th>
            <th scope="col">Customer Name</th>
            <th scope="col">Order Date</th>
            <th scope="col">Delivered Amount (AUD)</th>
            <th scope="col">Total Amount (AUD)</th>
          </tr>
        </thead>
        <tbody>
          <!--iterating over orders -->
          <tr v-for="order in pageOfItems" :key="order.id">
            <td>{{ order[0] }}</td>
            <td>{{ order[4] }}</td>
            <td>{{ order[1] }}</td>
            <td v-if="order[3]">${{ order[3] }}</td>
            <td v-else>-</td>
            <td v-if="order[2]">${{ order[2] }}</td>
            <td v-else>-</td>
          </tr>
        </tbody>
      </table>
    </center>
    <br /><br />
    <center>
      <!--pagination using jw-pagination -->
      <jw-pagination
        :pageSize="5"
        :items="orders"
        @changePage="onChangePage"
      ></jw-pagination>
    </center>
  </div>
</template>

<style>
#search-button {
  width: 150px;
  height: 45px;
}

#search-text {
  width: 60%;
  height: 45px;
  margin-right: 2px;
  margin-left: 45px;
}

#order-table {
  text-align: center;
  width: 93%;
  justify-self: center;
  border: solid;
  border-color: grey;
}
</style>

<script>
import axios from "axios";
export default {
  name: "Orders",

  data() {
    return {
      pageOfItems: [],
      orders: [],
      filter: {
        filt: "",
        success: true,
      },
      date: {
        startdate: null,
        enddate: null,
      },
    };
  },
  methods: {
    //get all orders from backend
    getOrders() {
      const path = "http://localhost:5000/orders";
      axios
        .get(path)
        .then((res) => {
          this.orders = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    onChangePage(pageOfItems) {
      // update page of items
      this.pageOfItems = pageOfItems;
    },
    //get filtered order for search
    filterOrders(property) {
      const path = `http://localhost:5000/filterOrders`;
      console.log("yellow");
      console.log(property);
      axios
        .post(path, property)
        .then((res) => {
          this.orders = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    // get filtered orders for date creation
    filterByDate(dates) {
      const path = `http://localhost:5000/filterByDate`;
      axios
        .post(path, dates)
        .then((res) => {
          this.orders = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    //on search submit filter orders
    onSubmit(e) {
      e.preventDefault();
      this.filterOrders(this.filter);
    },
    //on date change filter orders
    onChange(e) {
      e.preventDefault();
      this.filterByDate(this.date);
    },
  },
  created() {
    this.getOrders();
  },
};
</script>
