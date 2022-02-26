import database from "../modules/database";
import app from "../modules/app";
import { XMLParser, XMLValidator } from "fast-xml-parser";
import xsdSchemaValidator from "xsd-schema-validator";
import fs from "fs";

const main = async () => {
  await database.run();
  await app.run();

  const PORT: number = 6060;
  app.app.listen(process.env.PORT || PORT, function () {
    console.log(`server listening on port ${this.address().port}`);
  });
};

main();
