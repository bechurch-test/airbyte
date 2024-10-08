/*
 * Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.integrations.destination.iceberg.hive;

import static io.airbyte.integrations.destination.iceberg.IcebergIntegrationTestUtil.ICEBERG_IMAGE_NAME;

import com.fasterxml.jackson.databind.JsonNode;
import io.airbyte.cdk.integrations.standardtest.destination.DestinationAcceptanceTest;
import io.airbyte.integrations.destination.iceberg.IcebergIntegrationTestUtil;
import io.airbyte.integrations.destination.iceberg.config.format.DataFileFormat;
import io.airbyte.integrations.destination.iceberg.container.HiveMetastoreS3PostgresCompose;
import java.util.HashSet;
import java.util.List;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Disabled;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * @author Leibniz on 2022/11/3.
 */
@Disabled("We will not be supporting Hive meta store going forward, tests are broken too")
public class IcebergHiveCatalogS3AvroIntegrationTest extends DestinationAcceptanceTest {

  private static final Logger LOGGER = LoggerFactory.getLogger(IcebergHiveCatalogS3AvroIntegrationTest.class);

  /**
   * start-up of hive metastore server takes minutes (including pg table initializing) so put the
   * docker-compose environment here as a static member, only start once
   */
  private static HiveMetastoreS3PostgresCompose metastoreCompose;

  private static JsonNode config;

  @BeforeAll
  public static void startCompose() {
    metastoreCompose = new HiveMetastoreS3PostgresCompose();
    metastoreCompose.start();
    config = metastoreCompose.getComposeConfig(DataFileFormat.AVRO);
    IcebergIntegrationTestUtil.createS3WarehouseBucket(config);
    LOGGER.info("==> Started Hive Metastore docker compose containers...");

  }

  @AfterAll
  public static void stopCompose() {
    IcebergIntegrationTestUtil.stopAndCloseContainer(metastoreCompose, "Hive Metastore");
  }

  @Override
  protected void setup(final TestDestinationEnv testEnv, final HashSet<String> TEST_SCHEMAS) {}

  @Override
  protected void tearDown(final TestDestinationEnv testEnv) {}

  @Override
  protected String getImageName() {
    return ICEBERG_IMAGE_NAME;
  }

  @Override
  protected JsonNode getConfig() {
    return config;
  }

  @Override
  protected JsonNode getFailCheckConfig() {
    return metastoreCompose.getWrongConfig();
  }

  @Override
  protected List<JsonNode> retrieveRecords(final TestDestinationEnv testEnv,
                                           final String streamName,
                                           final String namespace,
                                           final JsonNode streamSchema)
      throws Exception {
    return IcebergIntegrationTestUtil.retrieveRecords(getConfig(), namespace, streamName);
  }

}
