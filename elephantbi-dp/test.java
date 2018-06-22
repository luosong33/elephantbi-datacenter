// ORM class for table 'test'
// WARNING: This class is AUTO-GENERATED. Modify at your own risk.
//
// Debug information:
// Generated date: Tue Jun 19 16:55:35 CST 2018
// For connector: org.apache.sqoop.manager.MySQLManager
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapred.lib.db.DBWritable;
import com.cloudera.sqoop.lib.JdbcWritableBridge;
import com.cloudera.sqoop.lib.DelimiterSet;
import com.cloudera.sqoop.lib.FieldFormatter;
import com.cloudera.sqoop.lib.RecordParser;
import com.cloudera.sqoop.lib.BooleanParser;
import com.cloudera.sqoop.lib.BlobRef;
import com.cloudera.sqoop.lib.ClobRef;
import com.cloudera.sqoop.lib.LargeObjectLoader;
import com.cloudera.sqoop.lib.SqoopRecord;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.sql.Date;
import java.sql.Time;
import java.sql.Timestamp;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class test extends SqoopRecord  implements DBWritable, Writable {
  private final int PROTOCOL_VERSION = 3;
  public int getClassFormatVersion() { return PROTOCOL_VERSION; }
  public static interface FieldSetterCommand {    void setField(Object value);  }  protected ResultSet __cur_result_set;
  private Map<String, FieldSetterCommand> setters = new HashMap<String, FieldSetterCommand>();
  private void init0() {
    setters.put("id", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.id = (Long)value;
      }
    });
    setters.put("name", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.name = (String)value;
      }
    });
    setters.put("age", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.age = (Integer)value;
      }
    });
    setters.put("gmt_create", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.gmt_create = (java.sql.Timestamp)value;
      }
    });
    setters.put("gmt_modified", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.gmt_modified = (java.sql.Timestamp)value;
      }
    });
    setters.put("addr", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.addr = (String)value;
      }
    });
    setters.put("phoen", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.phoen = (String)value;
      }
    });
    setters.put("qq", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.qq = (Integer)value;
      }
    });
    setters.put("weixin", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.weixin = (String)value;
      }
    });
    setters.put("weibo", new FieldSetterCommand() {
      @Override
      public void setField(Object value) {
        test.this.weibo = (String)value;
      }
    });
  }
  public test() {
    init0();
  }
  private Long id;
  public Long get_id() {
    return id;
  }
  public void set_id(Long id) {
    this.id = id;
  }
  public test with_id(Long id) {
    this.id = id;
    return this;
  }
  private String name;
  public String get_name() {
    return name;
  }
  public void set_name(String name) {
    this.name = name;
  }
  public test with_name(String name) {
    this.name = name;
    return this;
  }
  private Integer age;
  public Integer get_age() {
    return age;
  }
  public void set_age(Integer age) {
    this.age = age;
  }
  public test with_age(Integer age) {
    this.age = age;
    return this;
  }
  private java.sql.Timestamp gmt_create;
  public java.sql.Timestamp get_gmt_create() {
    return gmt_create;
  }
  public void set_gmt_create(java.sql.Timestamp gmt_create) {
    this.gmt_create = gmt_create;
  }
  public test with_gmt_create(java.sql.Timestamp gmt_create) {
    this.gmt_create = gmt_create;
    return this;
  }
  private java.sql.Timestamp gmt_modified;
  public java.sql.Timestamp get_gmt_modified() {
    return gmt_modified;
  }
  public void set_gmt_modified(java.sql.Timestamp gmt_modified) {
    this.gmt_modified = gmt_modified;
  }
  public test with_gmt_modified(java.sql.Timestamp gmt_modified) {
    this.gmt_modified = gmt_modified;
    return this;
  }
  private String addr;
  public String get_addr() {
    return addr;
  }
  public void set_addr(String addr) {
    this.addr = addr;
  }
  public test with_addr(String addr) {
    this.addr = addr;
    return this;
  }
  private String phoen;
  public String get_phoen() {
    return phoen;
  }
  public void set_phoen(String phoen) {
    this.phoen = phoen;
  }
  public test with_phoen(String phoen) {
    this.phoen = phoen;
    return this;
  }
  private Integer qq;
  public Integer get_qq() {
    return qq;
  }
  public void set_qq(Integer qq) {
    this.qq = qq;
  }
  public test with_qq(Integer qq) {
    this.qq = qq;
    return this;
  }
  private String weixin;
  public String get_weixin() {
    return weixin;
  }
  public void set_weixin(String weixin) {
    this.weixin = weixin;
  }
  public test with_weixin(String weixin) {
    this.weixin = weixin;
    return this;
  }
  private String weibo;
  public String get_weibo() {
    return weibo;
  }
  public void set_weibo(String weibo) {
    this.weibo = weibo;
  }
  public test with_weibo(String weibo) {
    this.weibo = weibo;
    return this;
  }
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof test)) {
      return false;
    }
    test that = (test) o;
    boolean equal = true;
    equal = equal && (this.id == null ? that.id == null : this.id.equals(that.id));
    equal = equal && (this.name == null ? that.name == null : this.name.equals(that.name));
    equal = equal && (this.age == null ? that.age == null : this.age.equals(that.age));
    equal = equal && (this.gmt_create == null ? that.gmt_create == null : this.gmt_create.equals(that.gmt_create));
    equal = equal && (this.gmt_modified == null ? that.gmt_modified == null : this.gmt_modified.equals(that.gmt_modified));
    equal = equal && (this.addr == null ? that.addr == null : this.addr.equals(that.addr));
    equal = equal && (this.phoen == null ? that.phoen == null : this.phoen.equals(that.phoen));
    equal = equal && (this.qq == null ? that.qq == null : this.qq.equals(that.qq));
    equal = equal && (this.weixin == null ? that.weixin == null : this.weixin.equals(that.weixin));
    equal = equal && (this.weibo == null ? that.weibo == null : this.weibo.equals(that.weibo));
    return equal;
  }
  public boolean equals0(Object o) {
    if (this == o) {
      return true;
    }
    if (!(o instanceof test)) {
      return false;
    }
    test that = (test) o;
    boolean equal = true;
    equal = equal && (this.id == null ? that.id == null : this.id.equals(that.id));
    equal = equal && (this.name == null ? that.name == null : this.name.equals(that.name));
    equal = equal && (this.age == null ? that.age == null : this.age.equals(that.age));
    equal = equal && (this.gmt_create == null ? that.gmt_create == null : this.gmt_create.equals(that.gmt_create));
    equal = equal && (this.gmt_modified == null ? that.gmt_modified == null : this.gmt_modified.equals(that.gmt_modified));
    equal = equal && (this.addr == null ? that.addr == null : this.addr.equals(that.addr));
    equal = equal && (this.phoen == null ? that.phoen == null : this.phoen.equals(that.phoen));
    equal = equal && (this.qq == null ? that.qq == null : this.qq.equals(that.qq));
    equal = equal && (this.weixin == null ? that.weixin == null : this.weixin.equals(that.weixin));
    equal = equal && (this.weibo == null ? that.weibo == null : this.weibo.equals(that.weibo));
    return equal;
  }
  public void readFields(ResultSet __dbResults) throws SQLException {
    this.__cur_result_set = __dbResults;
    this.id = JdbcWritableBridge.readLong(1, __dbResults);
    this.name = JdbcWritableBridge.readString(2, __dbResults);
    this.age = JdbcWritableBridge.readInteger(3, __dbResults);
    this.gmt_create = JdbcWritableBridge.readTimestamp(4, __dbResults);
    this.gmt_modified = JdbcWritableBridge.readTimestamp(5, __dbResults);
    this.addr = JdbcWritableBridge.readString(6, __dbResults);
    this.phoen = JdbcWritableBridge.readString(7, __dbResults);
    this.qq = JdbcWritableBridge.readInteger(8, __dbResults);
    this.weixin = JdbcWritableBridge.readString(9, __dbResults);
    this.weibo = JdbcWritableBridge.readString(10, __dbResults);
  }
  public void readFields0(ResultSet __dbResults) throws SQLException {
    this.id = JdbcWritableBridge.readLong(1, __dbResults);
    this.name = JdbcWritableBridge.readString(2, __dbResults);
    this.age = JdbcWritableBridge.readInteger(3, __dbResults);
    this.gmt_create = JdbcWritableBridge.readTimestamp(4, __dbResults);
    this.gmt_modified = JdbcWritableBridge.readTimestamp(5, __dbResults);
    this.addr = JdbcWritableBridge.readString(6, __dbResults);
    this.phoen = JdbcWritableBridge.readString(7, __dbResults);
    this.qq = JdbcWritableBridge.readInteger(8, __dbResults);
    this.weixin = JdbcWritableBridge.readString(9, __dbResults);
    this.weibo = JdbcWritableBridge.readString(10, __dbResults);
  }
  public void loadLargeObjects(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void loadLargeObjects0(LargeObjectLoader __loader)
      throws SQLException, IOException, InterruptedException {
  }
  public void write(PreparedStatement __dbStmt) throws SQLException {
    write(__dbStmt, 0);
  }

  public int write(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeLong(id, 1 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(name, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeInteger(age, 3 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeTimestamp(gmt_create, 4 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(gmt_modified, 5 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeString(addr, 6 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(phoen, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeInteger(qq, 8 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeString(weixin, 9 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(weibo, 10 + __off, 12, __dbStmt);
    return 10;
  }
  public void write0(PreparedStatement __dbStmt, int __off) throws SQLException {
    JdbcWritableBridge.writeLong(id, 1 + __off, -5, __dbStmt);
    JdbcWritableBridge.writeString(name, 2 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeInteger(age, 3 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeTimestamp(gmt_create, 4 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeTimestamp(gmt_modified, 5 + __off, 93, __dbStmt);
    JdbcWritableBridge.writeString(addr, 6 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(phoen, 7 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeInteger(qq, 8 + __off, 4, __dbStmt);
    JdbcWritableBridge.writeString(weixin, 9 + __off, 12, __dbStmt);
    JdbcWritableBridge.writeString(weibo, 10 + __off, 12, __dbStmt);
  }
  public void readFields(DataInput __dataIn) throws IOException {
this.readFields0(__dataIn);  }
  public void readFields0(DataInput __dataIn) throws IOException {
    if (__dataIn.readBoolean()) { 
        this.id = null;
    } else {
    this.id = Long.valueOf(__dataIn.readLong());
    }
    if (__dataIn.readBoolean()) { 
        this.name = null;
    } else {
    this.name = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.age = null;
    } else {
    this.age = Integer.valueOf(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.gmt_create = null;
    } else {
    this.gmt_create = new Timestamp(__dataIn.readLong());
    this.gmt_create.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.gmt_modified = null;
    } else {
    this.gmt_modified = new Timestamp(__dataIn.readLong());
    this.gmt_modified.setNanos(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.addr = null;
    } else {
    this.addr = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.phoen = null;
    } else {
    this.phoen = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.qq = null;
    } else {
    this.qq = Integer.valueOf(__dataIn.readInt());
    }
    if (__dataIn.readBoolean()) { 
        this.weixin = null;
    } else {
    this.weixin = Text.readString(__dataIn);
    }
    if (__dataIn.readBoolean()) { 
        this.weibo = null;
    } else {
    this.weibo = Text.readString(__dataIn);
    }
  }
  public void write(DataOutput __dataOut) throws IOException {
    if (null == this.id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.id);
    }
    if (null == this.name) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, name);
    }
    if (null == this.age) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.age);
    }
    if (null == this.gmt_create) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.gmt_create.getTime());
    __dataOut.writeInt(this.gmt_create.getNanos());
    }
    if (null == this.gmt_modified) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.gmt_modified.getTime());
    __dataOut.writeInt(this.gmt_modified.getNanos());
    }
    if (null == this.addr) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, addr);
    }
    if (null == this.phoen) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, phoen);
    }
    if (null == this.qq) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.qq);
    }
    if (null == this.weixin) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, weixin);
    }
    if (null == this.weibo) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, weibo);
    }
  }
  public void write0(DataOutput __dataOut) throws IOException {
    if (null == this.id) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.id);
    }
    if (null == this.name) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, name);
    }
    if (null == this.age) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.age);
    }
    if (null == this.gmt_create) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.gmt_create.getTime());
    __dataOut.writeInt(this.gmt_create.getNanos());
    }
    if (null == this.gmt_modified) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeLong(this.gmt_modified.getTime());
    __dataOut.writeInt(this.gmt_modified.getNanos());
    }
    if (null == this.addr) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, addr);
    }
    if (null == this.phoen) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, phoen);
    }
    if (null == this.qq) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    __dataOut.writeInt(this.qq);
    }
    if (null == this.weixin) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, weixin);
    }
    if (null == this.weibo) { 
        __dataOut.writeBoolean(true);
    } else {
        __dataOut.writeBoolean(false);
    Text.writeString(__dataOut, weibo);
    }
  }
  private static final DelimiterSet __outputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  public String toString() {
    return toString(__outputDelimiters, true);
  }
  public String toString(DelimiterSet delimiters) {
    return toString(delimiters, true);
  }
  public String toString(boolean useRecordDelim) {
    return toString(__outputDelimiters, useRecordDelim);
  }
  public String toString(DelimiterSet delimiters, boolean useRecordDelim) {
    StringBuilder __sb = new StringBuilder();
    char fieldDelim = delimiters.getFieldsTerminatedBy();
    __sb.append(FieldFormatter.escapeAndEnclose(id==null?"null":"" + id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(name==null?"null":name, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(age==null?"null":"" + age, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(gmt_create==null?"null":"" + gmt_create, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(gmt_modified==null?"null":"" + gmt_modified, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(addr==null?"null":addr, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(phoen==null?"null":phoen, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(qq==null?"null":"" + qq, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(weixin==null?"null":weixin, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(weibo==null?"null":weibo, delimiters));
    if (useRecordDelim) {
      __sb.append(delimiters.getLinesTerminatedBy());
    }
    return __sb.toString();
  }
  public void toString0(DelimiterSet delimiters, StringBuilder __sb, char fieldDelim) {
    __sb.append(FieldFormatter.escapeAndEnclose(id==null?"null":"" + id, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(name==null?"null":name, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(age==null?"null":"" + age, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(gmt_create==null?"null":"" + gmt_create, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(gmt_modified==null?"null":"" + gmt_modified, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(addr==null?"null":addr, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(phoen==null?"null":phoen, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(qq==null?"null":"" + qq, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(weixin==null?"null":weixin, delimiters));
    __sb.append(fieldDelim);
    __sb.append(FieldFormatter.escapeAndEnclose(weibo==null?"null":weibo, delimiters));
  }
  private static final DelimiterSet __inputDelimiters = new DelimiterSet((char) 44, (char) 10, (char) 0, (char) 0, false);
  private RecordParser __parser;
  public void parse(Text __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharSequence __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(byte [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(char [] __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(ByteBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  public void parse(CharBuffer __record) throws RecordParser.ParseError {
    if (null == this.__parser) {
      this.__parser = new RecordParser(__inputDelimiters);
    }
    List<String> __fields = this.__parser.parseRecord(__record);
    __loadFromFields(__fields);
  }

  private void __loadFromFields(List<String> fields) {
    Iterator<String> __it = fields.listIterator();
    String __cur_str = null;
    try {
    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.id = null; } else {
      this.id = Long.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.name = null; } else {
      this.name = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.age = null; } else {
      this.age = Integer.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.gmt_create = null; } else {
      this.gmt_create = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.gmt_modified = null; } else {
      this.gmt_modified = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.addr = null; } else {
      this.addr = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.phoen = null; } else {
      this.phoen = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.qq = null; } else {
      this.qq = Integer.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.weixin = null; } else {
      this.weixin = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.weibo = null; } else {
      this.weibo = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  private void __loadFromFields0(Iterator<String> __it) {
    String __cur_str = null;
    try {
    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.id = null; } else {
      this.id = Long.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.name = null; } else {
      this.name = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.age = null; } else {
      this.age = Integer.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.gmt_create = null; } else {
      this.gmt_create = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.gmt_modified = null; } else {
      this.gmt_modified = java.sql.Timestamp.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.addr = null; } else {
      this.addr = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.phoen = null; } else {
      this.phoen = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null") || __cur_str.length() == 0) { this.qq = null; } else {
      this.qq = Integer.valueOf(__cur_str);
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.weixin = null; } else {
      this.weixin = __cur_str;
    }

    if (__it.hasNext()) {
        __cur_str = __it.next();
    } else {
        __cur_str = "null";
    }
    if (__cur_str.equals("null")) { this.weibo = null; } else {
      this.weibo = __cur_str;
    }

    } catch (RuntimeException e) {    throw new RuntimeException("Can't parse input data: '" + __cur_str + "'", e);    }  }

  public Object clone() throws CloneNotSupportedException {
    test o = (test) super.clone();
    o.gmt_create = (o.gmt_create != null) ? (java.sql.Timestamp) o.gmt_create.clone() : null;
    o.gmt_modified = (o.gmt_modified != null) ? (java.sql.Timestamp) o.gmt_modified.clone() : null;
    return o;
  }

  public void clone0(test o) throws CloneNotSupportedException {
    o.gmt_create = (o.gmt_create != null) ? (java.sql.Timestamp) o.gmt_create.clone() : null;
    o.gmt_modified = (o.gmt_modified != null) ? (java.sql.Timestamp) o.gmt_modified.clone() : null;
  }

  public Map<String, Object> getFieldMap() {
    Map<String, Object> __sqoop$field_map = new HashMap<String, Object>();
    __sqoop$field_map.put("id", this.id);
    __sqoop$field_map.put("name", this.name);
    __sqoop$field_map.put("age", this.age);
    __sqoop$field_map.put("gmt_create", this.gmt_create);
    __sqoop$field_map.put("gmt_modified", this.gmt_modified);
    __sqoop$field_map.put("addr", this.addr);
    __sqoop$field_map.put("phoen", this.phoen);
    __sqoop$field_map.put("qq", this.qq);
    __sqoop$field_map.put("weixin", this.weixin);
    __sqoop$field_map.put("weibo", this.weibo);
    return __sqoop$field_map;
  }

  public void getFieldMap0(Map<String, Object> __sqoop$field_map) {
    __sqoop$field_map.put("id", this.id);
    __sqoop$field_map.put("name", this.name);
    __sqoop$field_map.put("age", this.age);
    __sqoop$field_map.put("gmt_create", this.gmt_create);
    __sqoop$field_map.put("gmt_modified", this.gmt_modified);
    __sqoop$field_map.put("addr", this.addr);
    __sqoop$field_map.put("phoen", this.phoen);
    __sqoop$field_map.put("qq", this.qq);
    __sqoop$field_map.put("weixin", this.weixin);
    __sqoop$field_map.put("weibo", this.weibo);
  }

  public void setField(String __fieldName, Object __fieldVal) {
    if (!setters.containsKey(__fieldName)) {
      throw new RuntimeException("No such field:"+__fieldName);
    }
    setters.get(__fieldName).setField(__fieldVal);
  }

}
