import * as React from "react";
import Card from "@mui/joy/Card";
import CardContent from "@mui/joy/CardContent";
import Divider from "@mui/joy/Divider";
import CardOverflow from "@mui/joy/CardOverflow";
import Typography from "@mui/joy/Typography";
import { Box, Button, Stack } from "@mui/joy";

function test() {
  console.log("click");
}
const NestedCard = ({ title, description }) => {
  return (
    <Box onClick={test} sx={{ borderRadius: 0, width: 350, maxWidth: "100%", mx: "40px", mt: "20px", mb: "10px" }}>
      <Card sx={{ borderRadius: 0, width: 350 }}>
        <Button color="neutral" onClick={test} variant="plain">
          <CardContent sx={{ width: "100%", padding: 0 }}>
            {/* <Typography level="body-xs">IN DESIGN</Typography> */}
            <Typography level="title-lg">{title}</Typography>
          </CardContent>
        </Button>
        <Button color="neutral" onClick={test} variant="plain">
          <Card orientation="horizontal" size="sm" sx={{ width: 300, bgcolor: "background.surface", borderRadius: 0, mb: 1 }}>
            <CardContent>
              {/* <Typography level="title-md">Sub project</Typography> */}
              <Typography level="body-sm">{description}</Typography>
              <Typography level="body-sm">......blablabla......</Typography>
            </CardContent>
          </Card>
        </Button>
        <CardOverflow
          variant="soft"
          sx={{
            display: "flex",
            flexDirection: "row",
            gap: 1,
            justifyContent: "space-around",
            py: 1,
            borderTop: "1px solid",
            borderColor: "divider",
            padding: 0,
          }}
        >
          <Stack direction="row" sx={{ padding: 0, maxHeight: "70%" }}>
            <Button variant="plain" onClick={test} sx={{ width: 175, margin: 0, padding: 0 }}>
              this is a button
            </Button>
            <Divider orientation="vertical" sx={{ margin: 0 }} />
            <Button variant="plain" onClick={test} sx={{ width: 175, margin: 0, padding: 0 }}>
              this is also a button
            </Button>
          </Stack>
        </CardOverflow>
      </Card>
    </Box>
  );
};

{
  /* <Button variant="text" onClick={console.log("click")}>
            13
          </Button>
          <Divider orientation="vertical" />
          <Typography startDecorator={<CommentOutlinedIcon />} level="title-sm">
            9
          </Typography> */
}
export default NestedCard;
