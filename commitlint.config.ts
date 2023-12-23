import { RuleConfigSeverity, UserConfig } from "@commitlint/types";

const Configuration: UserConfig = {
  extends: ["@commitlint/config-angular"],
  rules: {
    "type-enum": [
      RuleConfigSeverity.Error,
      "always",
      [
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "test",
        "revert",
        "chore",
        "ci",
        "build",
      ],
    ],
  },
};

export default Configuration;
