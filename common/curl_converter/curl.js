import * as curlconverter from 'curlconverter';

function convertToPython(curl) {

    const result = curlconverter.toPython(curl);

    console.log(result);

}
const curlCommand = process.argv[2];
convertToPython(curlCommand);