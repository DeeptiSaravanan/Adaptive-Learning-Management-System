const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const csvWriter = createCsvWriter({
  path: 'newinput.csv',
  header: [
    {id: 'Time', title: 'Time'},
    {id: 'Level', title: 'Level'},
    {id: 'Mode', title: 'Mode'},
    {id: 'NewRate', title: 'NewRate'},
    {id: 'Rate', title: 'Rate'},
    {id: 'Output', title: 'Output'},
  ]
});

var data = [
  {
    Time: $final_count,
    Level: '0',
    Mode: '0',
    NewRate: '0',
    Rate: '0',
    Output: '0'
  }
];

csvWriter
  .writeRecords(data)
  .then(()=> console.log('The CSV file was written successfully'));


