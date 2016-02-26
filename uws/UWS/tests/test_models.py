# -*- coding: utf-8 -*-
import unittest

from uws import UWS


class JobListTest(unittest.TestCase):
    def setUp(self):
        self.xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<uws:jobs xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink">
  <uws:jobref id="2014-06-03T15:33:29:4235" xlink:href="https://www.cosmosim.org/uws/query/335912448787925" xlink:type="simple">
    <uws:phase>COMPLETED</uws:phase>
  </uws:jobref>
  <uws:jobref id="2014-06-02T10:14:25:1677" xlink:href="https://www.cosmosim.org/uws/query/308893189727250" xlink:type="simple">
    <uws:phase>ABORTED</uws:phase>
  </uws:jobref>
  <uws:jobref id="2014-05-28T10:46:39:2755" xlink:href="https://www.cosmosim.org/uws/query/198796714554760" xlink:type="simple">
    <uws:phase>COMPLETED</uws:phase>
  </uws:jobref>
  <uws:jobref id="2014-05-09T15:13:50:6896" xlink:href="https://www.cosmosim.org/uws/query/1177277256137938" xlink:type="simple">
    <uws:phase>ERROR</uws:phase>
  </uws:jobref>
  <uws:jobref id="rndSamp2" xlink:href="https://www.cosmosim.org/uws/query/356246647522833857" xlink:type="simple">
    <uws:phase>COMPLETED</uws:phase>
  </uws:jobref>
</uws:jobs>
        '''[1:]

    def test(self):
        job_list = UWS.models.Jobs(self.xml)

        self.assertEqual(len(job_list.job_reference), 5)

        job_list_str = "Job '2014-06-03T15:33:29:4235' in phase 'COMPLETED' - https://www.cosmosim.org/uws/query/335912448787925\nJob '2014-06-02T10:14:25:1677' in phase 'ABORTED' - https://www.cosmosim.org/uws/query/308893189727250\nJob '2014-05-28T10:46:39:2755' in phase 'COMPLETED' - https://www.cosmosim.org/uws/query/198796714554760\nJob '2014-05-09T15:13:50:6896' in phase 'ERROR' - https://www.cosmosim.org/uws/query/1177277256137938\nJob 'rndSamp2' in phase 'COMPLETED' - https://www.cosmosim.org/uws/query/356246647522833857\n"
        self.assertEqual(str(job_list), job_list_str)

        job1 = job_list.job_reference[0]
        self.assertEqual(job1.id, '2014-06-03T15:33:29:4235')
        self.assertEqual(job1.phase, ['COMPLETED'])
        self.assertEqual(job1.reference.type, "simple")
        self.assertEqual(job1.reference.href, "https://www.cosmosim.org/uws/query/335912448787925")

        job2 = job_list.job_reference[1]
        self.assertEqual(job2.id, '2014-06-02T10:14:25:1677')
        self.assertEqual(job2.phase, ['ABORTED'])
        self.assertEqual(job2.reference.type, "simple")
        self.assertEqual(job2.reference.href, "https://www.cosmosim.org/uws/query/308893189727250")

        job3 = job_list.job_reference[2]
        self.assertEqual(job3.id, '2014-05-28T10:46:39:2755')
        self.assertEqual(job3.phase, ['COMPLETED'])
        self.assertEqual(job3.reference.type, "simple")
        self.assertEqual(job3.reference.href, "https://www.cosmosim.org/uws/query/198796714554760")

        job4 = job_list.job_reference[3]
        self.assertEqual(job4.id, '2014-05-09T15:13:50:6896')
        self.assertEqual(job4.phase, ['ERROR'])
        self.assertEqual(job4.reference.type, "simple")
        self.assertEqual(job4.reference.href, "https://www.cosmosim.org/uws/query/1177277256137938")

        job5 = job_list.job_reference[4]
        self.assertEqual(job5.id, u'rndSamp2')
        self.assertEqual(job5.phase, ['COMPLETED'])
        self.assertEqual(job5.reference.type, "simple")
        self.assertEqual(job5.reference.href, "https://www.cosmosim.org/uws/query/356246647522833857")


class CompletedJobTest(unittest.TestCase):
    def setUp(self):
        self.xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<uws:job xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink">
  <uws:jobId>335912448787925</uws:jobId>
  <uws:ownerId>adrian</uws:ownerId>
  <uws:phase>COMPLETED</uws:phase>
  <uws:quote xsi:nil="true"/>
  <uws:startTime>2014-06-03T15:33:30+02:00</uws:startTime>
  <uws:endTime>2014-06-03T15:33:31+02:00</uws:endTime>
  <uws:executionDuration>30</uws:executionDuration>
  <uws:destruction>2999-12-31T00:00:00+01:00</uws:destruction>
  <uws:parameters>
    <uws:parameter id="database">cosmosim_user_adrian</uws:parameter>
    <uws:parameter id="table">2014-06-03T15:33:29:4235</uws:parameter>
    <uws:parameter id="query">SELECT 0.25*(0.5+FLOOR(LOG10(Mvir)/0.25)) AS log_mass, COUNT(*) AS num&#13;
FROM MDR1.BDMV&#13;
WHERE snapnum=85 &#13;
GROUP BY FLOOR(LOG10(Mvir)/0.25)&#13;
ORDER BY log_mass
-- The query plan used to run this query: --
--------------------------------------------
--
-- CALL paquExec('SELECT 0.25 * ( 0.5 + FLOOR( LOG10( `Mvir` ) / 0.25 ) ) AS `log_mass`,COUNT(*) AS `num`,FLOOR( LOG10( `Mvir` ) / 0.25 ) AS `_FLOOR_LOG10_Mvir_/_0__25_` FROM MDR1.BDMV WHERE ( `snapnum` = 85 )  GROUP BY FLOOR( LOG10( Mvir ) / 0.25 )  ', 'aggregation_tmp_75797262')
-- USE spider_tmp_shard
-- SET @i=0
-- CREATE TABLE cosmosim_user_adrian.`2014-06-03T15:33:29:4235` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,  `log_mass`,SUM(`num`) AS `num`&#13; FROM `aggregation_tmp_75797262`  GROUP BY `_FLOOR_LOG10_Mvir_/_0__25_` ORDER BY `log_mass` ASC 
-- CALL paquDropTmp('aggregation_tmp_75797262')
</uws:parameter>
    <uws:parameter id="queue">short</uws:parameter>
  </uws:parameters>
  <uws:results>
    <uws:result id="csv" xlink:href="https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/csv" xlink:type="simple"/>
    <uws:result id="votable.xml" xlink:href="https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votable" xlink:type="simple"/>
    <uws:result id="votableB1.xml" xlink:href="https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votableB1" xlink:type="simple"/>
    <uws:result id="votableB2.xml" xlink:href="https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votableB2" xlink:type="simple"/>
  </uws:results>
</uws:job>
        '''[1:]

    def test(self):
        job = UWS.models.Job(self.xml)

        job_str = "JobId : '335912448787925'\nRunId : 'None'\nOwnerId : 'adrian'\nPhase : 'COMPLETED'\nQuote : 'None'\nCreationTime : 'None'\nStartTime : '2014-06-03T15:33:30+02:00'\nEndTime : '2014-06-03T15:33:31+02:00'\nExecutionDuration : '30'\nDestruction : '2999-12-31T00:00:00+01:00'\nParameters :\nParameter id 'database' byRef: False is_post: False - value: cosmosim_user_adrian\nParameter id 'table' byRef: False is_post: False - value: 2014-06-03T15:33:29:4235\nParameter id 'query' byRef: False is_post: False - value: SELECT 0.25*(0.5+FLOOR(LOG10(Mvir)/0.25)) AS log_mass, COUNT(*) AS num\r\nFROM MDR1.BDMV\r\nWHERE snapnum=85 \r\nGROUP BY FLOOR(LOG10(Mvir)/0.25)\r\nORDER BY log_mass\n-- The query plan used to run this query: --\n--------------------------------------------\n--\n-- CALL paquExec('SELECT 0.25 * ( 0.5 + FLOOR( LOG10( `Mvir` ) / 0.25 ) ) AS `log_mass`,COUNT(*) AS `num`,FLOOR( LOG10( `Mvir` ) / 0.25 ) AS `_FLOOR_LOG10_Mvir_/_0__25_` FROM MDR1.BDMV WHERE ( `snapnum` = 85 )  GROUP BY FLOOR( LOG10( Mvir ) / 0.25 )  ', 'aggregation_tmp_75797262')\n-- USE spider_tmp_shard\n-- SET @i=0\n-- CREATE TABLE cosmosim_user_adrian.`2014-06-03T15:33:29:4235` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,  `log_mass`,SUM(`num`) AS `num`\r FROM `aggregation_tmp_75797262`  GROUP BY `_FLOOR_LOG10_Mvir_/_0__25_` ORDER BY `log_mass` ASC \n-- CALL paquDropTmp('aggregation_tmp_75797262')\n\nParameter id 'queue' byRef: False is_post: False - value: short\nResults :\nResult id 'csv' reference: https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/csv\nResult id 'votable.xml' reference: https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votable\nResult id 'votableB1.xml' reference: https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votableB1\nResult id 'votableB2.xml' reference: https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votableB2\nerrorSummary :\n False\njobInfo :\n"
        self.assertEqual(str(job), job_str)

        self.assertEqual(job.job_id, '335912448787925')
        self.assertEqual(job.run_id, None)
        self.assertEqual(job.owner_id, 'adrian')
        self.assertEqual(job.phase, ['COMPLETED'])
        self.assertEqual(job.quote, None)
        self.assertEqual(job.start_time, '2014-06-03T15:33:30+02:00')
        self.assertEqual(job.end_time, '2014-06-03T15:33:31+02:00')
        self.assertEqual(job.execution_duration, 30)
        self.assertEqual(job.destruction, '2999-12-31T00:00:00+01:00')

        # check parameters
        param = job.parameters[0]
        self.assertEqual(param.id, 'database')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        self.assertEqual(param.value, 'cosmosim_user_adrian')

        param = job.parameters[1]
        self.assertEqual(param.id, 'table')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        self.assertEqual(param.value, '2014-06-03T15:33:29:4235')

        param = job.parameters[2]
        self.assertEqual(param.id, 'query')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        query_value = "SELECT 0.25*(0.5+FLOOR(LOG10(Mvir)/0.25)) AS log_mass, COUNT(*) AS num\r\nFROM MDR1.BDMV\r\nWHERE snapnum=85 \r\nGROUP BY FLOOR(LOG10(Mvir)/0.25)\r\nORDER BY log_mass\n-- The query plan used to run this query: --\n--------------------------------------------\n--\n-- CALL paquExec('SELECT 0.25 * ( 0.5 + FLOOR( LOG10( `Mvir` ) / 0.25 ) ) AS `log_mass`,COUNT(*) AS `num`,FLOOR( LOG10( `Mvir` ) / 0.25 ) AS `_FLOOR_LOG10_Mvir_/_0__25_` FROM MDR1.BDMV WHERE ( `snapnum` = 85 )  GROUP BY FLOOR( LOG10( Mvir ) / 0.25 )  ', 'aggregation_tmp_75797262')\n-- USE spider_tmp_shard\n-- SET @i=0\n-- CREATE TABLE cosmosim_user_adrian.`2014-06-03T15:33:29:4235` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,  `log_mass`,SUM(`num`) AS `num`\r FROM `aggregation_tmp_75797262`  GROUP BY `_FLOOR_LOG10_Mvir_/_0__25_` ORDER BY `log_mass` ASC \n-- CALL paquDropTmp('aggregation_tmp_75797262')\n"
        self.assertEqual(param.value, query_value)

        param = job.parameters[3]
        self.assertEqual(param.id, 'queue')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        self.assertEqual(param.value, 'short')

        # check results
        result = job.results[0]
        self.assertEqual(result.id, 'csv')
        self.assertEqual(result.reference.type, 'simple')
        self.assertEqual(result.reference.href, 'https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/csv')

        result = job.results[1]
        self.assertEqual(result.id, 'votable.xml')
        self.assertEqual(result.reference.type, 'simple')
        self.assertEqual(result.reference.href, 'https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votable')

        result = job.results[2]
        self.assertEqual(result.id, 'votableB1.xml')
        self.assertEqual(result.reference.type, 'simple')
        self.assertEqual(result.reference.href, 'https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votableB1')

        result = job.results[3]
        self.assertEqual(result.id, 'votableB2.xml')
        self.assertEqual(result.reference.type, 'simple')
        self.assertEqual(result.reference.href, 'https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votableB2')

        self.assertEqual(job.error_summary, False)
        self.assertEqual(job.job_info, [])


class AbortedJobTest(unittest.TestCase):
    def setUp(self):
        self.xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<uws:job xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <uws:jobId>308893189727250</uws:jobId>
  <uws:ownerId>adrian</uws:ownerId>
  <uws:phase>ABORTED</uws:phase>
  <uws:quote xsi:nil="true"/>
  <uws:startTime>2014-06-02T10:14:25+02:00</uws:startTime>
  <uws:endTime>2014-06-02T10:14:55+02:00</uws:endTime>
  <uws:executionDuration>30</uws:executionDuration>
  <uws:destruction>2999-12-31T00:00:00+01:00</uws:destruction>
  <uws:parameters>
    <uws:parameter id="database">cosmosim_user_adrian</uws:parameter>
    <uws:parameter id="table">2014-06-02T10:14:25:1677</uws:parameter>
    <uws:parameter id="query">select count(*) from MDR1.Particles85 where x &lt; 1
-- The query plan used to run this query: --
--------------------------------------------
--
-- CALL paquExec('SELECT COUNT(*) AS `_count_*_` FROM MDR1.Particles85 WHERE ( `x` &lt; 1 )   ', 'aggregation_tmp_49645551')
-- USE spider_tmp_shard
-- SET @i=0
-- CREATE TABLE cosmosim_user_adrian.`2014-06-02T10:14:25:1677` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,  SUM(`_count_*_`) AS `_count_*_`&#13; FROM `aggregation_tmp_49645551`   
-- CALL paquDropTmp('aggregation_tmp_49645551')
</uws:parameter>
    <uws:parameter id="queue">short</uws:parameter>
  </uws:parameters>
  <uws:results/>
</uws:job>
        '''[1:]

    def test(self):
        job = UWS.models.Job(self.xml)

        job_str = "JobId : '308893189727250'\nRunId : 'None'\nOwnerId : 'adrian'\nPhase : 'ABORTED'\nQuote : 'None'\nCreationTime : 'None'\nStartTime : '2014-06-02T10:14:25+02:00'\nEndTime : '2014-06-02T10:14:55+02:00'\nExecutionDuration : '30'\nDestruction : '2999-12-31T00:00:00+01:00'\nParameters :\nParameter id 'database' byRef: False is_post: False - value: cosmosim_user_adrian\nParameter id 'table' byRef: False is_post: False - value: 2014-06-02T10:14:25:1677\nParameter id 'query' byRef: False is_post: False - value: select count(*) from MDR1.Particles85 where x < 1\n-- The query plan used to run this query: --\n--------------------------------------------\n--\n-- CALL paquExec('SELECT COUNT(*) AS `_count_*_` FROM MDR1.Particles85 WHERE ( `x` < 1 )   ', 'aggregation_tmp_49645551')\n-- USE spider_tmp_shard\n-- SET @i=0\n-- CREATE TABLE cosmosim_user_adrian.`2014-06-02T10:14:25:1677` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,  SUM(`_count_*_`) AS `_count_*_`\r FROM `aggregation_tmp_49645551`   \n-- CALL paquDropTmp('aggregation_tmp_49645551')\n\nParameter id 'queue' byRef: False is_post: False - value: short\nResults :\nerrorSummary :\n False\njobInfo :\n"
        self.assertEqual(str(job), job_str)

        self.assertEqual(job.job_id, '308893189727250')
        self.assertEqual(job.run_id, None)
        self.assertEqual(job.owner_id, 'adrian')
        self.assertEqual(job.phase, ['ABORTED'])
        self.assertEqual(job.quote, None)
        self.assertEqual(job.start_time, '2014-06-02T10:14:25+02:00')
        self.assertEqual(job.end_time, '2014-06-02T10:14:55+02:00')
        self.assertEqual(job.execution_duration, 30)
        self.assertEqual(job.destruction, '2999-12-31T00:00:00+01:00')

        # check parameters
        param = job.parameters[0]
        self.assertEqual(param.id, 'database')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        self.assertEqual(param.value, 'cosmosim_user_adrian')

        param = job.parameters[1]
        self.assertEqual(param.id, 'table')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        self.assertEqual(param.value, '2014-06-02T10:14:25:1677')

        param = job.parameters[2]
        self.assertEqual(param.id, 'query')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        query_value = "select count(*) from MDR1.Particles85 where x < 1\n-- The query plan used to run this query: --\n--------------------------------------------\n--\n-- CALL paquExec('SELECT COUNT(*) AS `_count_*_` FROM MDR1.Particles85 WHERE ( `x` < 1 )   ', 'aggregation_tmp_49645551')\n-- USE spider_tmp_shard\n-- SET @i=0\n-- CREATE TABLE cosmosim_user_adrian.`2014-06-02T10:14:25:1677` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,  SUM(`_count_*_`) AS `_count_*_`\r FROM `aggregation_tmp_49645551`   \n-- CALL paquDropTmp('aggregation_tmp_49645551')\n"
        self.assertEqual(param.value, query_value)

        param = job.parameters[3]
        self.assertEqual(param.id, 'queue')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        self.assertEqual(param.value, 'short')

        self.assertEqual(job.results, [])
        self.assertEqual(job.error_summary, False)
        self.assertEqual(job.job_info, [])


class ErroredJobTest(unittest.TestCase):
    def setUp(self):
        self.xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<uws:job xmlns:uws="http://www.ivoa.net/xml/UWS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <uws:jobId>1177277256137938</uws:jobId>
  <uws:ownerId>adrian</uws:ownerId>
  <uws:phase>ERROR</uws:phase>
  <uws:quote xsi:nil="true"/>
  <uws:startTime>2014-05-09T15:13:48+02:00</uws:startTime>
  <uws:endTime>2014-05-09T15:13:48+02:00</uws:endTime>
  <uws:executionDuration>30</uws:executionDuration>
  <uws:destruction>2999-12-31T00:00:00+01:00</uws:destruction>
  <uws:parameters>
    <uws:parameter id="database">cosmosim_user_adrian</uws:parameter>
    <uws:parameter id="table">2014-05-09T15:13:50:6896</uws:parameter>
    <uws:parameter id="query">select avg(x) from `MDPL`.`Particles88tmp`;
-- The query plan used to run this query: --
--------------------------------------------
--
-- CALL paquExec('SELECT  COUNT(x) AS `cnt_avg(x)`, SUM(x) AS `sum_avg(x)` FROM `MDPL`.`Particles88tmp` ', 'aggregation_tmp_9424512')
-- USE spider_tmp_shard
-- SET @i=0
-- CREATE TABLE cosmosim_user_adrian.`2014-05-09T15:13:50:6896` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,   (SUM(`sum_avg(x)`) / SUM(`cnt_avg(x)`)) AS `avg(x)`&#13; FROM `aggregation_tmp_9424512`   
-- CALL paquDropTmp('aggregation_tmp_9424512')
</uws:parameter>
    <uws:parameter id="queue">short</uws:parameter>
  </uws:parameters>
  <uws:results/>
  <uws:errorSummary type="transient" hasDetail="false">
    <uws:message>Remote MySQL server has gone away</uws:message>
  </uws:errorSummary>
</uws:job>
        '''[1:]

    def test(self):
        job = UWS.models.Job(self.xml)

        job_str = "JobId : '1177277256137938'\nRunId : 'None'\nOwnerId : 'adrian'\nPhase : 'ERROR'\nQuote : 'None'\nCreationTime : 'None'\nStartTime : '2014-05-09T15:13:48+02:00'\nEndTime : '2014-05-09T15:13:48+02:00'\nExecutionDuration : '30'\nDestruction : '2999-12-31T00:00:00+01:00'\nParameters :\nParameter id 'database' byRef: False is_post: False - value: cosmosim_user_adrian\nParameter id 'table' byRef: False is_post: False - value: 2014-05-09T15:13:50:6896\nParameter id 'query' byRef: False is_post: False - value: select avg(x) from `MDPL`.`Particles88tmp`;\n-- The query plan used to run this query: --\n--------------------------------------------\n--\n-- CALL paquExec('SELECT  COUNT(x) AS `cnt_avg(x)`, SUM(x) AS `sum_avg(x)` FROM `MDPL`.`Particles88tmp` ', 'aggregation_tmp_9424512')\n-- USE spider_tmp_shard\n-- SET @i=0\n-- CREATE TABLE cosmosim_user_adrian.`2014-05-09T15:13:50:6896` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,   (SUM(`sum_avg(x)`) / SUM(`cnt_avg(x)`)) AS `avg(x)`\r FROM `aggregation_tmp_9424512`   \n-- CALL paquDropTmp('aggregation_tmp_9424512')\n\nParameter id 'queue' byRef: False is_post: False - value: short\nResults :\nerrorSummary :\n Error Summary - type 'transient' hasDetail: False - message: Remote MySQL server has gone away\njobInfo :\n"
        self.assertEqual(str(job), job_str)

        self.assertEqual(job.job_id, '1177277256137938')
        self.assertEqual(job.run_id, None)
        self.assertEqual(job.owner_id, 'adrian')
        self.assertEqual(job.phase, ['ERROR'])
        self.assertEqual(job.quote, None)
        self.assertEqual(job.start_time, '2014-05-09T15:13:48+02:00')
        self.assertEqual(job.end_time, '2014-05-09T15:13:48+02:00')
        self.assertEqual(job.execution_duration, 30)
        self.assertEqual(job.destruction, '2999-12-31T00:00:00+01:00')

        # check parameters
        param = job.parameters[0]
        self.assertEqual(param.id, 'database')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        self.assertEqual(param.value, 'cosmosim_user_adrian')

        param = job.parameters[1]
        self.assertEqual(param.id, 'table')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        self.assertEqual(param.value, '2014-05-09T15:13:50:6896')

        param = job.parameters[2]
        self.assertEqual(param.id, 'query')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        query_value = "select avg(x) from `MDPL`.`Particles88tmp`;\n-- The query plan used to run this query: --\n--------------------------------------------\n--\n-- CALL paquExec('SELECT  COUNT(x) AS `cnt_avg(x)`, SUM(x) AS `sum_avg(x)` FROM `MDPL`.`Particles88tmp` ', 'aggregation_tmp_9424512')\n-- USE spider_tmp_shard\n-- SET @i=0\n-- CREATE TABLE cosmosim_user_adrian.`2014-05-09T15:13:50:6896` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,   (SUM(`sum_avg(x)`) / SUM(`cnt_avg(x)`)) AS `avg(x)`\r FROM `aggregation_tmp_9424512`   \n-- CALL paquDropTmp('aggregation_tmp_9424512')\n"
        self.assertEqual(param.value, query_value)

        param = job.parameters[3]
        self.assertEqual(param.id, 'queue')
        self.assertEqual(param.by_reference, False)
        self.assertEqual(param.is_post, False)
        self.assertEqual(param.value, 'short')

        self.assertEqual(job.results, [])

        error = job.error_summary
        self.assertEqual(error.type, 'transient')
        self.assertEqual(error.has_detail, False)
        self.assertEqual(len(error.messages), 1)
        self.assertEqual(error.messages[0], 'Remote MySQL server has gone away')

        self.assertEqual(job.job_info, [])


class JobListNamespaceTest(unittest.TestCase):
    def setUp(self):
        self.xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<jobs xmlns="http://www.ivoa.net/xml/UWS/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink">
  <jobref id="335912448787925" xlink:href="https://www.cosmosim.org/uws/query/335912448787925" xlink:type="simple">
    <phase>COMPLETED</phase>
  </jobref>
</jobs>
        '''[1:]

    def test(self):
        job_list = UWS.models.Jobs(self.xml)

        self.assertEqual(len(job_list.job_reference), 1)

        job_list_str = "Job '335912448787925' in phase 'COMPLETED' - https://www.cosmosim.org/uws/query/335912448787925\n"
        self.assertEqual(str(job_list), job_list_str)

        job1 = job_list.job_reference[0]
        self.assertEqual(job1.id, '335912448787925')
        self.assertEqual(job1.phase, ['COMPLETED'])
        self.assertEqual(job1.reference.type, "simple")
        self.assertEqual(job1.reference.href, "https://www.cosmosim.org/uws/query/335912448787925")


class JobListNamespace2Test(JobListNamespaceTest):
    def setUp(self):
        self.xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<u:jobs xmlns:u="http://www.ivoa.net/xml/UWS/v1.0" xmlns:xlink="http://www.w3.org/1999/xlink">
  <u:jobref id="335912448787925" xlink:href="https://www.cosmosim.org/uws/query/335912448787925" xlink:type="simple">
    <u:phase>COMPLETED</u:phase>
  </u:jobref>
</u:jobs>
        '''[1:]


class ErroredJobNamespaceTest(ErroredJobTest):
    def setUp(self):
        self.xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<job xmlns="http://www.ivoa.net/xml/UWS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <jobId>1177277256137938</jobId>
  <ownerId>adrian</ownerId>
  <phase>ERROR</phase>
  <quote xsi:nil="true"/>
  <startTime>2014-05-09T15:13:48+02:00</startTime>
  <endTime>2014-05-09T15:13:48+02:00</endTime>
  <executionDuration>30</executionDuration>
  <destruction>2999-12-31T00:00:00+01:00</destruction>
  <parameters>
    <parameter id="database">cosmosim_user_adrian</parameter>
    <parameter id="table">2014-05-09T15:13:50:6896</parameter>
    <parameter id="query">select avg(x) from `MDPL`.`Particles88tmp`;
-- The query plan used to run this query: --
--------------------------------------------
--
-- CALL paquExec('SELECT  COUNT(x) AS `cnt_avg(x)`, SUM(x) AS `sum_avg(x)` FROM `MDPL`.`Particles88tmp` ', 'aggregation_tmp_9424512')
-- USE spider_tmp_shard
-- SET @i=0
-- CREATE TABLE cosmosim_user_adrian.`2014-05-09T15:13:50:6896` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,   (SUM(`sum_avg(x)`) / SUM(`cnt_avg(x)`)) AS `avg(x)`&#13; FROM `aggregation_tmp_9424512`   
-- CALL paquDropTmp('aggregation_tmp_9424512')
</parameter>
    <parameter id="queue">short</parameter>
  </parameters>
  <results/>
  <errorSummary type="transient" hasDetail="false">
    <message>Remote MySQL server has gone away</message>
  </errorSummary>
</job>
        '''[1:]


class CompletedJobNamespaceTest(CompletedJobTest):
    def setUp(self):
        self.xml = '''
<?xml version="1.0" encoding="UTF-8"?>
<job xmlns="http://www.ivoa.net/xml/UWS/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink">
  <jobId>335912448787925</jobId>
  <ownerId>adrian</ownerId>
  <phase>COMPLETED</phase>
  <quote xsi:nil="true"/>
  <startTime>2014-06-03T15:33:30+02:00</startTime>
  <endTime>2014-06-03T15:33:31+02:00</endTime>
  <executionDuration>30</executionDuration>
  <destruction>2999-12-31T00:00:00+01:00</destruction>
  <parameters>
    <parameter id="database">cosmosim_user_adrian</parameter>
    <parameter id="table">2014-06-03T15:33:29:4235</parameter>
    <parameter id="query">SELECT 0.25*(0.5+FLOOR(LOG10(Mvir)/0.25)) AS log_mass, COUNT(*) AS num&#13;
FROM MDR1.BDMV&#13;
WHERE snapnum=85 &#13;
GROUP BY FLOOR(LOG10(Mvir)/0.25)&#13;
ORDER BY log_mass
-- The query plan used to run this query: --
--------------------------------------------
--
-- CALL paquExec('SELECT 0.25 * ( 0.5 + FLOOR( LOG10( `Mvir` ) / 0.25 ) ) AS `log_mass`,COUNT(*) AS `num`,FLOOR( LOG10( `Mvir` ) / 0.25 ) AS `_FLOOR_LOG10_Mvir_/_0__25_` FROM MDR1.BDMV WHERE ( `snapnum` = 85 )  GROUP BY FLOOR( LOG10( Mvir ) / 0.25 )  ', 'aggregation_tmp_75797262')
-- USE spider_tmp_shard
-- SET @i=0
-- CREATE TABLE cosmosim_user_adrian.`2014-06-03T15:33:29:4235` ENGINE=MyISAM SELECT @i:=@i+1 AS `row_id`,  `log_mass`,SUM(`num`) AS `num`&#13; FROM `aggregation_tmp_75797262`  GROUP BY `_FLOOR_LOG10_Mvir_/_0__25_` ORDER BY `log_mass` ASC 
-- CALL paquDropTmp('aggregation_tmp_75797262')
</parameter>
    <parameter id="queue">short</parameter>
  </parameters>
  <results>
    <result id="csv" xlink:href="https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/csv" xlink:type="simple"/>
    <result id="votable.xml" xlink:href="https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votable" xlink:type="simple"/>
    <result id="votableB1.xml" xlink:href="https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votableB1" xlink:type="simple"/>
    <result id="votableB2.xml" xlink:href="https://www.cosmosim.org/query/download/stream/table/2014-06-03T15%3A33%3A29%3A4235/format/votableB2" xlink:type="simple"/>
  </results>
</job>
        '''[1:]

