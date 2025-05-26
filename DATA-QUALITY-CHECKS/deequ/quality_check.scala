import com.amazon.deequ.VerificationSuite
import com.amazon.deequ.checks.{Check, CheckLevel}
import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder().appName("DeequCheck").getOrCreate()
val data = spark.read.option("header", "true").csv("s3://data-validation-and-quality-checks/output/data.csv")

val verificationResult = VerificationSuite()
  .onData(data)
  .addCheck(
    Check(CheckLevel.Error, "Data Check")
      .hasSize(_ > 0)
      .isComplete("id")
      .isUnique("id")
  )
  .run()

verificationResult.saveJsonResults(spark, "s3://data-validation-and-quality-checks/deequ-results/")