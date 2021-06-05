window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    large_params_function: function (largeValue1, largeValue2) {
      return someTransform(largeValue1, largeValue2)
    }
  }
})

